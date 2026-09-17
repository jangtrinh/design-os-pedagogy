"""Restart the real local server, retaining state, events and request identity."""
import http.client
import json
import queue
import re
import subprocess
import sys
import tempfile
import threading
import unittest
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RehearsalProcessTests(unittest.TestCase):
    def launch(self, data):
        child = subprocess.Popen([sys.executable, "-B", str(ROOT / "run_rehearsal.py"),
                                  "--port", "0", "--data-dir", str(data)],
                                 cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = queue.Queue()
        def read():
            for line in child.stdout:
                output.put(line)
        thread = threading.Thread(target=read, daemon=True)
        thread.start()
        self.addCleanup(self.stop, child, thread)
        try:
            line = output.get(timeout=8)
        except queue.Empty:
            self.fail("Server did not announce a listening address")
        found = re.search(r"http://127\.0\.0\.1:(\d+)", line)
        self.assertIsNotNone(found, line)
        return child, thread, int(found.group(1))

    @staticmethod
    def stop(child, thread):
        if child.poll() is None:
            child.terminate()
            try:
                child.wait(timeout=4)
            except subprocess.TimeoutExpired:
                child.kill()
                child.wait(timeout=4)
        thread.join(timeout=2)
        child.stdout.close()
        child.stderr.close()

    def request(self, port, method, path, body=None):
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=4)
        try:
            payload = json.dumps(body).encode() if body is not None else None
            headers = {"Content-Type": "application/json"} if payload is not None else {}
            conn.request(method, path, payload, headers)
            response = conn.getresponse()
            result = json.loads(response.read())
            self.assertIn(response.status, (200, 201), result)
            return result
        finally:
            conn.close()

    def test_restart_preserves_committed_session_and_idempotency(self):
        with tempfile.TemporaryDirectory() as temp:
            data = Path(temp) / "sessions"
            first, thread, port = self.launch(data)
            body = {"case_id": "fraction-magnitude", "request_id": str(uuid.uuid4())}
            state = self.request(port, "POST", "/api/sessions", body)["session"]
            route = f"/api/sessions/{state['id']}"
            event = {"revision": 0, "type": "probe", "choice": "explain",
                     "text": "Em giải thích cách so sánh được không?", "request_id": str(uuid.uuid4())}
            saved = self.request(port, "POST", route + "/events", event)["session"]
            self.stop(first, thread)
            second, thread2, port2 = self.launch(data)
            reopened = self.request(port2, "GET", route)["session"]
            self.assertEqual(reopened, saved)
            self.assertEqual(self.request(port2, "POST", route + "/events", event)["session"], saved)
            replay = self.request(port2, "GET", route + "/replay")
            self.assertTrue(replay["matches_saved_state"])
            self.assertEqual(replay["event_count"], 2)
            self.stop(second, thread2)


if __name__ == "__main__":
    unittest.main()
