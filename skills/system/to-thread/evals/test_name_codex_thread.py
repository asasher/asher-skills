"""Exercise naming against a local fake app-server; no Codex worker starts."""
import contextlib
import importlib.util
import io
from pathlib import Path
import subprocess
import sys
import unittest
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/name-codex-thread.py"


class NamingTests(unittest.TestCase):
    def run_server(self, source):
        spec = importlib.util.spec_from_file_location("name_thread", SCRIPT)
        helper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(helper)
        children = []
        popen = subprocess.Popen

        def launch(*args, **kwargs):
            child = popen([sys.executable, "-c", source], **kwargs)
            children.append(child)
            return child

        stdout = io.StringIO()
        failure = None
        with mock.patch.object(helper, "REPLY_TIMEOUT_SECONDS", 0.5, create=True), mock.patch.object(
            helper, "STOP_TIMEOUT_SECONDS", 0.1, create=True
        ), mock.patch.object(helper.subprocess, "Popen", side_effect=launch), mock.patch.object(
            sys, "argv", [str(SCRIPT), "known-thread-uuid", "Name"]
        ), contextlib.redirect_stdout(stdout):
            try:
                helper.main()
            except SystemExit as error:
                failure = str(error)
        self.assertEqual(1, len(children))
        self.assertIsNotNone(children[0].returncode, "app-server must be reaped")
        return stdout.getvalue(), failure

    def test_silent_server_times_out_with_known_identity(self):
        # Finite sleep makes this test fail quickly even against the old helper.
        _, failure = self.run_server("import time; time.sleep(1.5)")
        self.assertIn("timed out", failure)
        self.assertIn("known-thread-uuid", failure)

    def test_partial_stdout_line_times_out_and_reaps_uncooperative_server(self):
        _, failure = self.run_server(
            "import signal, sys, time; signal.signal(signal.SIGTERM, signal.SIG_IGN); "
            "sys.stdout.write('{'); sys.stdout.flush(); time.sleep(1.5)"
        )
        self.assertIn("timed out", failure)
        self.assertIn("known-thread-uuid", failure)

    def test_protocol_error_keeps_uuid(self):
        _, failure = self.run_server(
            'print(\'{"id": 1, "error": "refused"}\', flush=True)'
        )
        self.assertIn("refused", failure)
        self.assertIn("known-thread-uuid", failure)

    def test_successful_name_after_initialize_and_notification(self):
        output, failure = self.run_server('''
import json, sys
for line in sys.stdin:
    msg = json.loads(line)
    if "id" in msg:
        print(json.dumps({"method": "notification"}), flush=True)
        print(json.dumps({"id": msg["id"], "result": {}}), flush=True)
''')
        self.assertIsNone(failure)
        self.assertIn("named known-thread-uuid", output)


if __name__ == "__main__":
    unittest.main()
