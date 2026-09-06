"""Backend contract tests; local HTTP only, no credentials or image service needed."""
import argparse
import base64
from contextlib import contextmanager, redirect_stdout, redirect_stderr
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import image_backends as backends
import codex_imagegen as generator
import extract_spritesheet as sprites


def png(size=(32, 20), noise=False):
    if noise:
        image = Image.fromarray(np.random.default_rng(7).integers(0, 256, (size[1], size[0], 3), dtype=np.uint8))
    else:
        image = Image.new("RGB", size, "magenta")
        draw = ImageDraw.Draw(image)
        draw.rectangle((3, 3, 9, 12), fill="green")
        if size[0] > 20:
            draw.rectangle((20, 3, 28, 12), fill="blue")
    result = io.BytesIO()
    image.save(result, "PNG")
    return result.getvalue()


def result(raw=None):
    return {"data": [{"b64_json": base64.b64encode(raw or png()).decode()}]}


@contextmanager
def gateway(responses):
    calls = []
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass
        def do_POST(self):
            calls.append((self.path, dict(self.headers), json.loads(self.rfile.read(int(self.headers["Content-Length"])))))
            status, payload = responses[min(len(calls) - 1, len(responses) - 1)]
            raw = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
            self.send_response(status)
            if status == 302:
                self.send_header("Location", "http://127.0.0.1:1/leak")
            self.end_headers()
            self.wfile.write(raw)
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}/v1", calls
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


def options(home, *flags):
    parser = argparse.ArgumentParser()
    backends.add_backend_arguments(parser)
    return parser.parse_args(["--codex-home", str(home), *flags])


class SelectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.home = Path(self.temp.name)
    def tearDown(self):
        self.temp.cleanup()

    def test_proxy_precedes_native_and_reads_shadow_auth_without_changes(self):
        config = 'model_provider="gateway"\n[model_providers.gateway]\nbase_url="http://127.0.0.1:8317/v1"\n'
        auth = '{"OPENAI_API_KEY":"gateway-secret", "tokens":{"access_token":"oauth-not-bearer"}}'
        (self.home / "config.toml").write_text(config)
        (self.home / "auth.json").write_text(auth)
        backend = backends.resolve_backend(options(self.home), {}, native_available=True)
        self.assertEqual((backend.name, backend.key), ("cliproxyapi", "gateway-secret"))
        self.assertNotIn("gateway-secret", repr(backend))
        self.assertEqual((self.home / "config.toml").read_text(), config)
        self.assertEqual((self.home / "auth.json").read_text(), auth)

    def test_env_proxy_uses_gateway_key_without_platform_key(self):
        backend = backends.resolve_backend(options(self.home, "--proxy-url", "http://localhost:8317/v1", "--proxy-key-env", "LOCAL_GATEWAY_KEY"), {"LOCAL_GATEWAY_KEY": "proxy-key"})
        self.assertEqual(backend.key, "proxy-key")
        self.assertEqual(backend.model, "gpt-image-2")

    def test_openai_environment_pair_can_represent_gateway(self):
        backend = backends.resolve_backend(options(self.home), {"OPENAI_BASE_URL": "http://localhost:8317/v1", "OPENAI_API_KEY": "gateway-key"})
        self.assertEqual(backend.name, "cliproxyapi")
        self.assertEqual(backend.key, "gateway-key")

    def test_missing_proxy_credentials_stop_before_native(self):
        with self.assertRaisesRegex(backends.BackendError, "Gateway key unavailable"):
            backends.resolve_backend(options(self.home, "--proxy-url", "http://localhost:8317/v1"), {}, native_available=True)

    def test_oauth_is_not_proxy_key(self):
        (self.home / "config.toml").write_text('model_provider="gateway"\n[model_providers.gateway]\nbase_url="http://localhost:8317/v1"\n')
        (self.home / "auth.json").write_text('{"tokens":{"access_token":"oauth-secret"}}')
        with self.assertRaisesRegex(backends.BackendError, "OAuth tokens") as caught:
            backends.resolve_backend(options(self.home, "--proxy-url", "http://localhost:8317/v1"), {})
        self.assertNotIn("oauth-secret", str(caught.exception))

    def test_explicit_gateway_cannot_infer_key_from_another_endpoint(self):
        (self.home / "config.toml").write_text('model_provider="gateway"\n[model_providers.gateway]\nbase_url="https://configured.example/v1"\n')
        (self.home / "auth.json").write_text('{"OPENAI_API_KEY":"configured-secret"}')
        cases = [
            {},
            {"OPENAI_BASE_URL": "https://api.openai.com/v1", "OPENAI_API_KEY": "platform-secret"},
            {"OPENAI_BASE_URL": "https://configured.example/v1", "OPENAI_API_KEY": "environment-secret"},
            {"CLIPROXYAPI_BASE_URL": "https://configured.example/v1", "CLIPROXYAPI_API_KEY": "proxy-secret"},
            {"CLIPROXYAPI_BASE_URL": "https://configured.example/v1", "CLIPROXYAPI_KEY_ENV": "PROXY_KEY", "PROXY_KEY": "named-secret"},
        ]
        for env in cases:
            with self.subTest(env_names=list(env)), self.assertRaisesRegex(backends.BackendError, "selected endpoint") as caught:
                backends.resolve_backend(options(self.home, "--proxy-url", "https://unrelated.example/v1"), env)
            self.assertNotIn("secret", str(caught.exception))

    def test_inferred_credentials_require_matching_scheme_port_and_base_path(self):
        (self.home / "auth.json").write_text('{"OPENAI_API_KEY":"unbound-secret"}')
        env = {"OPENAI_BASE_URL": "https://configured.example/v1", "OPENAI_API_KEY": "environment-secret"}
        for url in ("https://configured.example:8443/v1", "https://configured.example/v2"):
            with self.subTest(url=url), self.assertRaises(backends.BackendError):
                backends.resolve_backend(options(self.home, "--proxy-url", url), env)
        with self.assertRaisesRegex(backends.BackendError, "selected endpoint"):
            backends.resolve_backend(options(self.home, "--proxy-url", "https://unrelated.example/v1"), {})
        self.assertFalse(backends._same_endpoint("http://localhost/v1", "https://localhost/v1"))

    def test_matching_explicit_gateway_can_reuse_bound_keys(self):
        env = {"OPENAI_BASE_URL": "https://configured.example/v1/", "OPENAI_API_KEY": "environment-secret"}
        backend = backends.resolve_backend(options(self.home, "--proxy-url", "https://CONFIGURED.example.:443/v1"), env)
        self.assertEqual(backend.key, "environment-secret")
        (self.home / "config.toml").write_text('model_provider="gateway"\n[model_providers.gateway]\nbase_url="https://configured.example/v1"\n')
        (self.home / "auth.json").write_text('{"OPENAI_API_KEY":"configured-secret"}')
        backend = backends.resolve_backend(options(self.home, "--proxy-url", "https://configured.example/v1/"), {})
        self.assertEqual(backend.key, "configured-secret")

    def test_explicit_key_source_authorizes_new_gateway_pairing(self):
        backend = backends.resolve_backend(options(self.home, "--proxy-url", "https://new.example/v1", "--proxy-key-env", "SELECTED_KEY"), {"SELECTED_KEY": "selected-secret", "OPENAI_BASE_URL": "https://old.example/v1", "OPENAI_API_KEY": "old-secret"})
        self.assertEqual(backend.key, "selected-secret")
        auth = self.home / "selected.json"
        auth.write_text('{"OPENAI_API_KEY":"selected-file-secret"}')
        backend = backends.resolve_backend(options(self.home, "--proxy-url", "https://new.example/v1", "--proxy-auth-file", str(auth)), {})
        self.assertEqual(backend.key, "selected-file-secret")

    def test_platform_trailing_dot_cannot_bypass_direct_permission(self):
        for url in ("https://api.openai.com./v1", "https://API.OPENAI.COM.:443/v1"):
            with self.subTest(url=url), self.assertRaisesRegex(backends.BackendError, "Platform endpoint"):
                backends.resolve_backend(options(self.home, "--backend", "cliproxyapi", "--proxy-url", url, "--proxy-key-env", "K"), {"K": "secret"})
            selected = backends.resolve_backend(options(self.home), {"OPENAI_BASE_URL": url, "OPENAI_API_KEY": "secret"}, native_available=True)
            self.assertEqual(selected.name, "native")
            with self.assertRaises(backends.BackendError):
                backends.resolve_backend(options(self.home), {"OPENAI_BASE_URL": url, "OPENAI_API_KEY": "secret"}, native_available=False)

    def test_native_without_proxy_and_direct_requires_permission(self):
        self.assertEqual(backends.resolve_backend(options(self.home), {"OPENAI_API_KEY": "key"}, True).name, "native")
        with self.assertRaisesRegex(backends.BackendError, "explicit user permission"):
            backends.resolve_backend(options(self.home, "--backend", "openai"), {"OPENAI_API_KEY": "key"})
        direct = backends.resolve_backend(options(self.home, "--allow-direct-api", "--api-key-env", "PLATFORM_KEY"), {"PLATFORM_KEY": "platform-key"}, False)
        self.assertEqual(direct.base_url, "https://api.openai.com/v1")

    def test_direct_will_not_reuse_gateway_environment_key(self):
        with self.assertRaisesRegex(backends.BackendError, "distinct OpenAI Platform-key"):
            backends.resolve_backend(options(self.home, "--backend", "openai", "--allow-direct-api"), {"OPENAI_BASE_URL": "http://localhost:8317/v1", "OPENAI_API_KEY": "proxy-key"})

    def test_url_credentials_and_remote_plaintext_rejected_safely(self):
        for url in ("https://user:secret@example.test/v1", "https://example.test/v1?key=secret", "http://example.test/v1"):
            with self.subTest(url=url), self.assertRaises(backends.BackendError) as caught:
                backends.resolve_backend(options(self.home, "--proxy-url", url, "--proxy-key-env", "K"), {"K": "secret"})
            self.assertNotIn("secret", str(caught.exception))


class RequestTests(unittest.TestCase):
    def test_http_auth_payload_decoding_and_dimension_mismatch_preserve_versions(self):
        with gateway([(200, result())]) as (url, calls), tempfile.TemporaryDirectory() as folder:
            backend = backends.Backend("cliproxyapi", url, "gateway-secret", quality="low")
            target = Path(folder) / "robot.png"
            target.write_bytes(b"previous")
            good, note, actual = generator.generate("robot", target, "robot", backend=backend, size=16)
            self.assertTrue(good)
            self.assertEqual(target.read_bytes(), b"previous")
            self.assertEqual(actual.name, "robot-v2.png")
            self.assertIn("requested=16x16; actual=32x20; dimension_mismatch=true", note)
            with Image.open(actual) as image:
                self.assertEqual(image.size, (32, 20))
            self.assertEqual(calls[0][0], "/v1/images/generations")
            self.assertEqual(calls[0][1]["Authorization"], "Bearer gateway-secret")
            self.assertEqual(calls[0][2], {"model": "gpt-image-2", "prompt": "robot", "n": 1, "size": "16x16", "quality": "low"})
            self.assertNotIn("gateway-secret", note)

    def test_failures_sanitized_and_single_request(self):
        cases = [(401, "credentials"), (403, "credentials"), (404, "model"), (400, "model support"), (422, "model support"), (429, "quota"), (504, "timed out"), (500, "service failed"), (302, "redirected")]
        for status, expected in cases:
            with self.subTest(status=status), gateway([(status, {"error": "secret-key raw server error"})]) as (url, calls):
                with self.assertRaisesRegex(backends.BackendError, expected) as caught:
                    backends.request_image(backends.Backend("cliproxyapi", url, "secret-key"), "robot", 16, 3)
                self.assertEqual(len(calls), 1)
                self.assertNotIn("secret-key", str(caught.exception))

    def test_missing_and_malformed_data(self):
        for payload in ({}, {"data": []}, {"data": [{"b64_json": "bad%%"}]}, result(b"not an image"), b"not json"):
            with self.subTest(payload=payload), gateway([(200, payload)]) as (url, calls):
                with self.assertRaises(backends.BackendError):
                    backends.request_image(backends.Backend("cliproxyapi", url, "key"), "robot", 16, 3)
                self.assertEqual(len(calls), 1)

    def test_unavailable_and_timeout_report_ambiguity_without_retry(self):
        for error, message in ((TimeoutError("secret"), "may have completed"), (ConnectionResetError("secret"), "may have started")):
            with self.subTest(error=error), patch.object(backends.urllib.request.OpenerDirector, "open", side_effect=error) as request:
                with self.assertRaisesRegex(backends.BackendError, message) as caught:
                    backends.request_image(backends.Backend("cliproxyapi", "http://localhost:1/v1", "secret"), "robot", 16, 1)
                self.assertEqual(request.call_count, 1)
                self.assertNotIn("secret", str(caught.exception))


class PipelineTests(unittest.TestCase):
    def test_layered_propagates_backend_records_dimensions_and_preserves_partial_evidence(self):
        with tempfile.TemporaryDirectory() as folder, gateway([(200, result()), (504, {})]) as (url, calls):
            root = Path(folder)
            scene = root / "scene.json"
            scene.write_text(json.dumps({"size": 16, "layers": [{"name": "backdrop", "role": "background", "subject": "forest"}, {"name": "hero", "subject": "robot"}]}))
            with redirect_stdout(io.StringIO()):
                good, note, path = generator.generate_layered(scene, root / "scene", backend=backends.Backend("cliproxyapi", url, "key"))
            self.assertFalse(good)
            manifest = json.loads((path / "manifest.json").read_text())
            self.assertEqual(manifest["status"], "failed")
            self.assertEqual(manifest["backend"], "cliproxyapi")
            self.assertEqual(manifest["layers"][0]["raw_size"], [32, 20])
            self.assertEqual(manifest["layers"][0]["size"], [16, 16])
            self.assertEqual(manifest["layers"][0]["resize_policy"], "stretch-to-canvas")
            self.assertTrue((path / manifest["layers"][0]["raw"]).exists())
            self.assertEqual(len(calls), 2)
            self.assertNotIn("key", manifest["error"])

    def test_layered_success_composites_and_versions_directory(self):
        with tempfile.TemporaryDirectory() as folder, gateway([(200, result())]) as (url, calls):
            root = Path(folder)
            (root / "scene.png").write_bytes(b"old flat")
            scene = root / "plan.json"
            scene.write_text(json.dumps({"size": 32, "layers": [{"name": "hero", "subject": "robot"}]}))
            with redirect_stdout(io.StringIO()):
                good, note, path = generator.generate_layered(scene, root / "scene", backend=backends.Backend("cliproxyapi", url, "key"))
            self.assertTrue(good)
            self.assertEqual(path.name, "scene-v2")
            self.assertTrue((path / "composite.png").exists())
            self.assertEqual(json.loads((path / "manifest.json").read_text())["status"], "complete")

    def test_batch_is_sequential_and_stops_at_first_failed_request(self):
        with tempfile.TemporaryDirectory() as folder, gateway([(200, result()), (401, {})]) as (url, calls):
            root = Path(folder)
            batch = root / "batch.json"
            batch.write_text(json.dumps([{"name": name, "subject": name} for name in ("first", "second", "third")]))
            argv = ["codex_imagegen.py", "--batch", str(batch), "--outdir", str(root), "--proxy-url", url, "--proxy-key-env", "TEST_GATEWAY_KEY"]
            with patch.object(sys, "argv", argv), patch.dict(generator.os.environ, {"TEST_GATEWAY_KEY": "key"}), redirect_stdout(io.StringIO()):
                code = generator.main()
            self.assertEqual(code, 1)
            self.assertEqual(len(calls), 2)
            self.assertIn("first", calls[0][2]["prompt"])
            self.assertIn("second", calls[1][2]["prompt"])
            self.assertTrue((root / "first.png").exists())
            self.assertFalse((root / "second.png").exists())

    def test_spritesheet_generation_propagates_backend_and_validates(self):
        with tempfile.TemporaryDirectory() as folder, gateway([(200, result(png((32, 16))))]) as (url, calls), redirect_stdout(io.StringIO()):
            manifest = sprites.extract(generate="two isolated items", out_dir=Path(folder) / "sprites", cols=2, rows=1, names="plant,rock", key="magenta", pad=1, validate=True, expect=2, backend=backends.Backend("cliproxyapi", url, "key"), generation_size=32)
            self.assertEqual(manifest["sheet"], {"width": 32, "height": 16})
            self.assertEqual(len(manifest["elements"]), 2)
            self.assertEqual(len(calls), 1)
            self.assertTrue((Path(manifest["artifact"]) / manifest["source"]["path"]).exists())

    def test_native_still_extracts_session_image_and_uses_selected_home(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "sessions").mkdir()
            encoded = base64.b64encode(png((100, 100), noise=True)).decode()
            def native_call(*args, **kwargs):
                self.assertEqual(kwargs["env"]["CODEX_HOME"], str(root))
                (root / "sessions" / "new.jsonl").write_text(json.dumps({"revised_prompt": "robot portrait", "image": encoded}) + "\n")
                return subprocess.CompletedProcess(args[0], 0, "", "")
            with patch.object(generator.subprocess, "run", side_effect=native_call):
                good, note, path = generator.generate("robot", root / "robot.png", "robot", backend=backends.Backend("native", codex_home=str(root)), size=100)
            self.assertTrue(good)
            self.assertIn("backend=native", note)
            self.assertTrue(path.exists())


if __name__ == "__main__":
    unittest.main()
