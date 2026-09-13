"""Resolve image backends and call an OpenAI-compatible Images API with stdlib HTTP.

Configuration is read-only. A resolved backend performs one request with no retries,
redirects, credential mutation, or provider fallback.
"""
from dataclasses import dataclass, field
import base64
import binascii
import io
import http.client
import json
import os
from pathlib import Path
import shutil
import socket
import urllib.error
import urllib.parse
import urllib.request

from PIL import Image, UnidentifiedImageError


class BackendError(RuntimeError):
    """A deliberately sanitized, actionable backend failure."""


@dataclass(frozen=True)
class Backend:
    name: str
    base_url: str = ""
    key: str = field(default="", repr=False)
    model: str = "gpt-image-2"
    quality: str | None = None
    codex_home: str | None = None


def add_backend_arguments(parser):
    parser.add_argument("--backend", choices=("auto", "cliproxyapi", "native", "openai"), default="auto")
    parser.add_argument("--proxy-url", help="Images API gateway base URL, normally ending in /v1")
    parser.add_argument("--proxy-key-env", help="environment variable containing the gateway bearer key")
    parser.add_argument("--proxy-auth-file", help="existing JSON file containing the gateway OPENAI_API_KEY")
    parser.add_argument("--codex-home", help="read the active provider and gateway auth from this Codex home")
    parser.add_argument("--allow-direct-api", action="store_true", help="explicit user permission for the direct OpenAI API")
    parser.add_argument("--api-key-env", default="OPENAI_API_KEY", help="direct OpenAI Platform key variable")
    parser.add_argument("--image-model", default="gpt-image-2", help="Images API model; native uses its session's image tool")
    parser.add_argument("--quality", choices=("auto", "low", "medium", "high"), help="requested Images API quality; provider may vary")


def _read_json_key(path):
    try:
        data = json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
        key = data.get("OPENAI_API_KEY") if isinstance(data, dict) else None
    except (OSError, ValueError):
        raise BackendError("Cannot read gateway credentials; check --proxy-auth-file and its JSON format.") from None
    if not isinstance(key, str) or not key.strip():
        raise BackendError("Gateway auth file needs a nonempty OPENAI_API_KEY; ChatGPT OAuth tokens are not gateway credentials.")
    return key.strip()


def _provider(home):
    config = home / "config.toml"
    if not config.exists():
        return {}
    try:
        import tomllib
        data = tomllib.loads(config.read_text(encoding="utf-8"))
        selected = data.get("model_provider", "openai")
        result = data.get("model_providers", {}).get(selected, {})
        if not isinstance(result, dict):
            raise ValueError()
        return result
    except ImportError:
        raise BackendError("Reading Codex config.toml requires Python 3.11+; pass --proxy-url and --proxy-key-env explicitly on older Python.") from None
    except (OSError, ValueError, TypeError, AttributeError):
        raise BackendError("Cannot read the active Codex provider; check config.toml or pass --proxy-url and a credential source explicitly.") from None


def _base_url(value):
    try:
        parsed = urllib.parse.urlsplit(value)
        # Never forward credentials through redirects or URL userinfo/query strings.
        if parsed.scheme not in ("http", "https") or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise ValueError()
        parsed.port
        if parsed.scheme == "http" and parsed.hostname not in ("localhost", "127.0.0.1", "::1"):
            raise BackendError("Use HTTPS for a remote gateway; plain HTTP is supported only on loopback.")
    except (ValueError, TypeError):
        raise BackendError("Invalid gateway URL; use an HTTP(S) base URL without credentials, query, or fragment.") from None
    return value.rstrip("/")


def _hostname(parsed):
    return (parsed.hostname or "").encode("idna").decode("ascii").lower().rstrip(".")


def _platform_url(value):
    try:
        return _hostname(urllib.parse.urlsplit(value)) == "api.openai.com"
    except (ValueError, UnicodeError, TypeError):
        return False


def _same_endpoint(left, right):
    """Bind inferred bearer keys to their configured API base, including its path."""
    if not left or not right:
        return False
    def identity(value):
        parsed = urllib.parse.urlsplit(value)
        if parsed.scheme not in ("http", "https") or not parsed.hostname or parsed.username is not None or parsed.password is not None or parsed.query or parsed.fragment:
            raise ValueError()
        return (parsed.scheme, _hostname(parsed), parsed.port or (443 if parsed.scheme == "https" else 80), parsed.path.rstrip("/"))
    try:
        return identity(left) == identity(right)
    except (ValueError, UnicodeError, TypeError):
        return False


def _environment_key(env, name):
    key = env.get(name, "").strip()
    if not key:
        raise BackendError("Selected gateway-key environment variable is empty; supply the existing gateway key or --proxy-auth-file.")
    return key


def _inferred_gateway_key(url, env, home, provider=None):
    # Inferred values belong to their configured endpoint. Explicit credential
    # flags are the user's way to authorize a different endpoint/source pairing.
    if _same_endpoint(url, env.get("CLIPROXYAPI_BASE_URL")):
        if env.get("CLIPROXYAPI_KEY_ENV"):
            return _environment_key(env, env["CLIPROXYAPI_KEY_ENV"])
        if env.get("CLIPROXYAPI_API_KEY"):
            return env["CLIPROXYAPI_API_KEY"].strip()
    if _same_endpoint(url, env.get("OPENAI_BASE_URL")) and env.get("OPENAI_API_KEY"):
        return env["OPENAI_API_KEY"].strip()
    provider = _provider(home) if provider is None else provider
    if _same_endpoint(url, provider.get("base_url")):
        if provider.get("env_key"):
            return _environment_key(env, provider["env_key"])
        if (home / "auth.json").exists():
            return _read_json_key(home / "auth.json")
    raise BackendError("Gateway key unavailable for the selected endpoint; choose --proxy-key-env or --proxy-auth-file explicitly. Inferred keys stay bound to their configured endpoint.")


def resolve_backend(args, environ=None, native_available=None):
    env = os.environ if environ is None else environ
    home = Path(args.codex_home or env.get("CODEX_HOME") or Path.home() / ".codex").expanduser()
    requested = args.backend
    if requested == "native":
        return Backend("native", codex_home=str(home))
    if requested == "openai":
        if not args.allow_direct_api:
            raise BackendError("Direct OpenAI API use requires explicit user permission via --allow-direct-api.")
        key = env.get(args.api_key_env, "").strip()
        if not key:
            raise BackendError("Direct OpenAI API key is unavailable; set the selected Platform-key environment variable.")
        # OPENAI_API_KEY often holds a proxy bearer key. Require a distinct variable
        # or unambiguous explicit source when the environment targets a gateway.
        configured_url = _provider(home).get("base_url") if args.api_key_env == "OPENAI_API_KEY" else None
        if args.api_key_env == "OPENAI_API_KEY" and (args.proxy_url or env.get("CLIPROXYAPI_BASE_URL") or (env.get("OPENAI_BASE_URL") and not _platform_url(env["OPENAI_BASE_URL"])) or (configured_url and not _platform_url(configured_url))):
            raise BackendError("OPENAI_API_KEY is associated with a gateway here; use --api-key-env with a distinct OpenAI Platform-key variable.")
        return Backend("openai", "https://api.openai.com/v1", key, args.image_model, args.quality)

    explicit_url = args.proxy_url or env.get("CLIPROXYAPI_BASE_URL")
    env_url = env.get("OPENAI_BASE_URL")
    provider = None if explicit_url or env_url else _provider(home)
    url = explicit_url or env_url or provider.get("base_url")
    proxy_selected = requested == "cliproxyapi" or (url and not _platform_url(url))
    if proxy_selected:
        if not url:
            raise BackendError("CLIProxyAPI needs --proxy-url, CLIPROXYAPI_BASE_URL, OPENAI_BASE_URL, or an active Codex provider base_url.")
        url = _base_url(url)
        if _platform_url(url):
            raise BackendError("The Platform endpoint is not a gateway; use --backend openai with --allow-direct-api and a Platform key.")
        if args.proxy_auth_file:
            key = _read_json_key(args.proxy_auth_file)
        elif args.proxy_key_env:
            key = _environment_key(env, args.proxy_key_env)
        else:
            key = _inferred_gateway_key(url, env, home, provider)
        return Backend("cliproxyapi", url, key, args.image_model, args.quality)

    if native_available is None:
        native_available = shutil.which("codex") is not None
    if native_available:
        return Backend("native", codex_home=str(home))
    if args.allow_direct_api:
        from copy import copy
        direct_args = copy(args)
        direct_args.backend = "openai"
        return resolve_backend(direct_args, env, native_available=False)
    raise BackendError("No configured gateway or Codex CLI found. Configure an existing gateway, use an available native session, or explicitly authorize a direct Platform API key.")


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def decode_image(encoded):
    if not isinstance(encoded, str) or not encoded:
        raise BackendError("Images API returned missing image data; check that this gateway/model supports base64 Images API results.")
    try:
        raw = base64.b64decode(encoded, validate=True)
        with Image.open(io.BytesIO(raw)) as opened:
            opened.load()
            dimensions = opened.size
            image = opened.convert("RGBA")
        if min(dimensions) <= 0:
            raise ValueError()
        output = io.BytesIO()
        image.save(output, "PNG")
    except (ValueError, OSError, binascii.Error, UnidentifiedImageError, Image.DecompressionBombError):
        raise BackendError("Images API returned malformed image data; response was not a decodable image. No output was written.") from None
    return output.getvalue(), dimensions


def request_image(backend, prompt, size, timeout):
    payload = {"model": backend.model, "prompt": prompt, "n": 1, "size": f"{size}x{size}"}
    if backend.quality:
        payload["quality"] = backend.quality
    try:
        request = urllib.request.Request(
            backend.base_url + "/images/generations",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization": "Bearer " + backend.key, "Content-Type": "application/json"},
            method="POST",
        )
        # Disable implicit environment forward proxies for configured gateways.
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), _NoRedirect())
        with opener.open(request, timeout=timeout) as response:
            data = json.loads(response.read())
    except urllib.error.HTTPError as exc:
        exc.close()
        if exc.code in (401, 403):
            note = "Gateway/API credentials rejected; verify the selected bearer key and its image permissions."
        elif exc.code == 404:
            note = "Images endpoint or model unavailable; check the base URL and advertised image models."
        elif exc.code in (400, 422):
            note = "Image request rejected; verify model support, requested size, and quality."
        elif exc.code in (408, 504):
            note = "Upstream image request timed out; generation may have completed. Inspect provider status before retrying."
        elif exc.code == 429:
            note = "Image service rate or quota limit reached; inspect provider limits before another request."
        elif 300 <= exc.code < 400:
            note = "Images endpoint redirected; use its final configured base URL. Credentials were not forwarded."
        else:
            note = "Image service failed; inspect gateway/upstream status before another request."
        raise BackendError(f"HTTP {exc.code}: {note} No retry or provider switch was attempted.") from None
    except (TimeoutError, socket.timeout):
        raise BackendError("Image request timed out; generation may have completed. No retry or provider switch was attempted; inspect provider status before retrying.") from None
    except (urllib.error.URLError, ConnectionError, OSError, http.client.HTTPException):
        raise BackendError("Image gateway unavailable or connection interrupted; check the configured URL, service, and TLS. Generation may have started; no retry or provider switch was attempted.") from None
    except (ValueError, UnicodeError):
        raise BackendError("Images API returned malformed JSON; check gateway Images API support. No retry or provider switch was attempted.") from None
    try:
        encoded = data["data"][0]["b64_json"]
    except (KeyError, IndexError, TypeError):
        raise BackendError("Images API returned missing image data; expected data[0].b64_json. No retry or provider switch was attempted.") from None
    return decode_image(encoded)
