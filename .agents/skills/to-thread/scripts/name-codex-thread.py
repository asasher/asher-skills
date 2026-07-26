#!/usr/bin/env python3
"""Name a Codex thread: one-shot `codex app-server` JSON-RPC `thread/name/set`.

Usage: name-codex-thread.py <thread-uuid> <name>

Verified against codex-cli 0.144.5. The app-server is experimental; if this
fails, leave the thread unnamed and hand the user its UUID instead.
"""
import json
import subprocess
import sys


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(__doc__.strip())
    thread_id, name = sys.argv[1], sys.argv[2]

    proc = subprocess.Popen(
        ["codex", "app-server"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL, text=True,
    )

    def send(msg: dict) -> None:
        proc.stdin.write(json.dumps(msg) + "\n")
        proc.stdin.flush()

    def await_reply(want_id: int) -> dict:
        while True:
            line = proc.stdout.readline()
            if not line:
                sys.exit("app-server closed the stream before replying")
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue
            if msg.get("id") == want_id:
                if "error" in msg:
                    sys.exit(f"app-server error: {msg['error']}")
                return msg.get("result", {})

    try:
        send({"jsonrpc": "2.0", "id": 1, "method": "initialize",
              "params": {"clientInfo": {"name": "to-thread", "version": "1.0"}}})
        await_reply(1)
        send({"jsonrpc": "2.0", "method": "initialized", "params": {}})
        send({"jsonrpc": "2.0", "id": 2, "method": "thread/name/set",
              "params": {"threadId": thread_id, "name": name}})
        await_reply(2)
        print(f"named {thread_id} -> {name!r}")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


if __name__ == "__main__":
    main()
