#!/usr/bin/env python3
"""Name a Codex thread: one-shot `codex app-server` JSON-RPC `thread/name/set`.

Usage: name-codex-thread.py <thread-uuid> <name>

The app-server is experimental and may drift between releases. If this fails,
leave the thread unnamed and hand the user its UUID instead.
"""
import json
import os
import selectors
import subprocess
import sys
import time


REPLY_TIMEOUT_SECONDS = 30
STOP_TIMEOUT_SECONDS = 5
MAX_REPLY_BYTES = 1024 * 1024


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(__doc__.strip())
    thread_id, name = sys.argv[1], sys.argv[2]
    proc = None
    try:
        proc = subprocess.Popen(
            ["codex", "app-server"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        deadline = time.monotonic() + REPLY_TIMEOUT_SECONDS
        pending = bytearray()

        def send(msg: dict) -> None:
            proc.stdin.write((json.dumps(msg) + "\n").encode())
            proc.stdin.flush()

        def await_reply(want_id: int) -> dict:
            with selectors.DefaultSelector() as selector:
                selector.register(proc.stdout, selectors.EVENT_READ)
                while True:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        raise TimeoutError("app-server reply timed out")
                    if b"\n" not in pending:
                        if not selector.select(remaining):
                            raise TimeoutError("app-server reply timed out")
                        chunk = os.read(proc.stdout.fileno(), 65536)
                        if not chunk:
                            raise RuntimeError("app-server closed the stream before replying")
                        pending.extend(chunk)
                        if len(pending) > MAX_REPLY_BYTES:
                            raise RuntimeError("app-server reply exceeded size limit")
                        continue
                    line, _, rest = pending.partition(b"\n")
                    pending[:] = rest
                    try:
                        msg = json.loads(line)
                    except (json.JSONDecodeError, UnicodeDecodeError):
                        continue
                    if isinstance(msg, dict) and msg.get("id") == want_id:
                        if "error" in msg:
                            raise RuntimeError(f"app-server error: {msg['error']}")
                        return msg.get("result", {})

        send({"jsonrpc": "2.0", "id": 1, "method": "initialize",
              "params": {"clientInfo": {"name": "to-thread", "version": "1.0"}}})
        await_reply(1)
        send({"jsonrpc": "2.0", "method": "initialized", "params": {}})
        send({"jsonrpc": "2.0", "id": 2, "method": "thread/name/set",
              "params": {"threadId": thread_id, "name": name}})
        await_reply(2)
        print(f"named {thread_id} -> {name!r}")
    except (OSError, RuntimeError) as error:
        sys.exit(f"could not name thread {thread_id}: {error}; resume by UUID")
    finally:
        if proc is not None:
            try:
                proc.terminate()
                try:
                    proc.wait(timeout=STOP_TIMEOUT_SECONDS)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait(timeout=STOP_TIMEOUT_SECONDS)
            finally:
                for stream in (proc.stdin, proc.stdout):
                    try:
                        stream.close()
                    except OSError:
                        pass


if __name__ == "__main__":
    main()
