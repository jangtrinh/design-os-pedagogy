"""Real HTTP checks over a temporary session database and actual UI assets."""

import http.client
import json
import tempfile
import threading
import unittest
import uuid
from pathlib import Path

from rehearsal.catalog import Catalog
from rehearsal.http_server import create_server
from rehearsal.store import Store

ROOT = Path(__file__).resolve().parent.parent


class RehearsalHttpTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.catalog = Catalog()
        self.store = Store(Path(self.temp.name) / "sessions.db", self.catalog)
        self.server = create_server(self.store, self.catalog, ROOT / "rehearsal" / "static")
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.cleanup)

    def cleanup(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        self.temp.cleanup()

    def request(self, method, path, data=None, headers=None, raw=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.server.server_address[1], timeout=3)
        body = json.dumps(data).encode() if data is not None else raw
        defaults = {"Content-Type": "application/json"} if body is not None else {}
        conn.request(method, path, body=body, headers={**defaults, **(headers or {})})
        response = conn.getresponse()
        result = response.status, dict(response.getheaders()), response.read()
        conn.close()
        return result

    def create(self):
        status, _, raw = self.request("POST", "/api/sessions", {"case_id": "fraction-magnitude", "request_id": str(uuid.uuid4())})
        self.assertEqual(status, 201)
        return json.loads(raw)["session"]

    def test_serves_actual_ui_and_declares_authored_mode(self):
        for path, mime in (("/", "text/html"), ("/app.js", "text/javascript"), ("/views.js", "text/javascript"), ("/styles.css", "text/css")):
            status, headers, body = self.request("GET", path)
            self.assertEqual(status, 200, path)
            self.assertIn(mime, headers["Content-Type"])
            self.assertGreater(len(body), 100)
            self.assertIn("frame-ancestors 'none'", headers["Content-Security-Policy"])
        status, _, body = self.request("GET", "/api/status")
        self.assertEqual(status, 200)
        self.assertFalse(json.loads(body)["model_calls"])

    def test_all_transitions_reload_replay_and_exports(self):
        state = self.create()
        for choice in ("explain", "tentative", "worked_example", "novel_reason", "continue", "probe", "save"):
            status, _, body = self.request("POST", f"/api/sessions/{state['id']}/events", {
                "type": state["phase"], "choice": choice, "text": "Tôi sẽ hỏi cách lập luận.",
                "revision": state["revision"], "request_id": str(uuid.uuid4())})
            self.assertEqual(status, 200, body)
            state = json.loads(body)["session"]
        status, _, body = self.request("GET", f"/api/sessions/{state['id']}")
        self.assertEqual(json.loads(body)["session"], state)
        status, _, body = self.request("GET", f"/api/sessions/{state['id']}/replay")
        self.assertTrue(json.loads(body)["matches_saved_state"])
        for format in ("md", "json"):
            status, headers, body = self.request("GET", f"/api/sessions/{state['id']}/export?format={format}")
            self.assertEqual(status, 200)
            self.assertIn("attachment", headers["Content-Disposition"])
            self.assertIn("Tôi sẽ hỏi", body.decode())

    def test_private_pack_keys_and_source_files_are_not_served(self):
        for path in ("/rehearsal/data/fractions.vi.json", "/data/fractions.vi.json", "/../README.md", "/%2e%2e/README.md", "/api/not-found"):
            self.assertEqual(self.request("GET", path)[0], 404)
        body = self.request("GET", "/api/catalog")[2]
        self.assertNotIn(b'"answer"', body)
        self.assertNotIn(b'"debrief"', body)

    def test_host_and_origin_boundaries(self):
        for headers in ({"Host": "attacker.example"}, {"Origin": "https://other.example"}, {"Sec-Fetch-Site": "cross-site"}):
            self.assertEqual(self.request("GET", "/api/status", headers=headers)[0], 403)

    def test_invalid_json_duplicate_keys_and_nonfinite_numbers(self):
        for raw in (b'{bad}', b'[]', b'{"a":1,"a":2}', b'{"a":NaN}', b'[' * 2000):
            self.assertEqual(self.request("POST", "/api/sessions", raw=raw)[0], 400)
        self.assertEqual(self.request("POST", "/api/sessions", raw=b'{}', headers={"Content-Type": "text/plain"})[0], 400)
        self.assertEqual(self.request("POST", "/api/sessions", raw=b'x' * (33*1024))[0], 413)
        self.assertEqual(self.store.list(), [])

    def test_http_conflict_preserves_latest_state(self):
        state = self.create()
        payload = {"type": "probe", "choice": "explain", "revision": 0, "request_id": str(uuid.uuid4())}
        self.assertEqual(self.request("POST", f"/api/sessions/{state['id']}/events", payload)[0], 200)
        payload["request_id"] = str(uuid.uuid4())
        status, _, body = self.request("POST", f"/api/sessions/{state['id']}/events", payload)
        self.assertEqual(status, 409)
        self.assertEqual(json.loads(body)["error"]["code"], "revision_conflict")
        self.assertEqual(self.store.get(state["id"])["revision"], 1)


if __name__ == "__main__":
    unittest.main()
