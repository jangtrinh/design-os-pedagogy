"""Verify bounded startup and database preservation using actual child processes."""
import hashlib
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

import test_rehearsal_process as server_tests

ROOT = Path(__file__).resolve().parents[1]


class StartupBoundaryTests(unittest.TestCase):
    def test_partial_stdout_cannot_extend_the_original_startup_deadline(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = Path(temporary)
            (fixture / "run_rehearsal.py").write_text(
                "import sys, time\n"
                "sys.stdout.write('Starting rehearsal without a newline')\n"
                "sys.stdout.flush()\n"
                "time.sleep(30)\n", encoding="utf-8")
            case = server_tests.RehearsalProcessTests(
                "test_restart_preserves_committed_session_and_idempotency")
            children = []
            original_popen = subprocess.Popen

            def record_child(*args, **kwargs):
                child = original_popen(*args, **kwargs)
                children.append(child)
                return child

            started = time.monotonic()
            try:
                with patch.object(server_tests, "ROOT", fixture), patch.object(
                        server_tests.subprocess, "Popen", side_effect=record_child):
                    with self.assertRaisesRegex(AssertionError, "did not announce"):
                        case.launch(fixture / "data")
            finally:
                case.doCleanups()
            self.assertLess(time.monotonic() - started, 15)
            self.assertEqual(len(children), 1)
            self.assertIsNotNone(children[0].poll())
            self.assertTrue(children[0].stdout.closed)
            self.assertTrue(children[0].stderr.closed)

    def test_corrupt_database_is_preserved_and_reported_without_traceback(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "rehearsal.sqlite3"
            target.write_bytes(b"This is not a SQLite database.\n")
            before = hashlib.sha256(target.read_bytes()).hexdigest()
            result = subprocess.run(
                [sys.executable, "-B", str(ROOT / "run_rehearsal.py"),
                 "--port", "0", "--data-dir", temporary], cwd=ROOT,
                text=True, capture_output=True, timeout=12)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Cannot start rehearsal", result.stderr)
            self.assertNotIn("Traceback", result.stderr)
            self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(), before)


if __name__ == "__main__":
    unittest.main()
