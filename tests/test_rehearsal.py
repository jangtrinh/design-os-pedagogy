"""Behavioral tests for authored practice, transaction boundaries and replay."""

import hashlib
import json
import os
import sqlite3
import tempfile
import unittest
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from rehearsal.catalog import Catalog, PACK_PATH
from rehearsal.errors import RehearsalError
from rehearsal.exporter import markdown
from rehearsal.store import Store


def key():
    return str(uuid.uuid4())


class RehearsalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "sessions.sqlite3"
        self.catalog = Catalog()
        self.store = Store(self.path, self.catalog)

    def create(self, case="fraction-magnitude", **extra):
        return self.store.write({"case_id": case, "request_id": key(), **extra})

    def move(self, state, choice, text="Lời của người dạy.", **extra):
        return self.store.write({"revision": state["revision"], "type": state["phase"],
                                 "choice": choice, "text": text, "request_id": key(), **extra}, state["id"])

    def advance(self, state, teach="number_line"):
        for choice in ("explain", "tentative", teach, "novel_reason", "continue"):
            state = self.move(state, choice)
        return state

    def test_three_cases_complete_restart_and_replay(self):
        for case_id in self.catalog.cases:
            with self.subTest(case=case_id):
                state = self.advance(self.create(case_id))
                self.assertEqual(state["phase"], "transfer")
                state = self.move(state, self.catalog.case(case_id)["transfer"]["answer"])
                state = self.move(state, "save", "Tôi sẽ hỏi thêm cách em lập luận.")
                self.assertEqual((state["phase"], state["revision"]), ("complete", 7))
                self.assertIsNone(state["prompt"])
                self.assertTrue(state["transfer_feedback"]["matched_authored_key"])
                restarted = Store(self.path, Catalog())
                self.assertEqual(restarted.get(state["id"]), state)
                self.assertTrue(restarted.replay(state["id"])["matches_saved_state"])
                self.assertEqual(len(restarted.history(state["id"])), 8)

    def test_every_instructional_strategy_has_explicit_responses(self):
        for case_id in self.catalog.cases:
            for teach in ("number_line", "worked_example", "rule_only"):
                for probe in ("explain", "represent", "rule"):
                    for check in ("novel_reason", "repeat", "praise"):
                        state = self.create(case_id)
                        for choice in (probe, "insufficient", teach, check):
                            state = self.move(state, choice)
                        self.assertEqual(state["phase"], "review")
                        self.assertTrue(all(isinstance(t["text"], str) for t in state["transcript"]))
                        self.assertEqual(len(state["review"]["observations"]), 4)

    def test_transfer_key_and_coaching_not_available_before_submission(self):
        public = json.dumps(self.catalog.public(), ensure_ascii=False)
        self.assertNotIn('"answer"', public)
        self.assertNotIn('probe_responses', public)
        state = self.create()
        secret = self.catalog.case(state["case_id"])["transfer"]["feedback"]
        for choice in ("explain", "tentative", "number_line", "novel_reason", "continue"):
            self.assertNotIn(secret, json.dumps(state, ensure_ascii=False))
            self.assertNotIn(secret, markdown(state))
            state = self.move(state, choice)
        self.assertNotIn("answer", state["prompt"])
        self.assertIsNone(state["transfer_feedback"])
        state = self.move(state, "accept")
        self.assertFalse(state["transfer_feedback"]["matched_authored_key"])
        self.assertEqual(state["transfer_feedback"]["explanation"], secret)

    def test_create_and_event_retry_are_idempotent(self):
        body = {"case_id": "fraction-magnitude", "request_id": key()}
        first = self.store.write(body)
        self.assertEqual(self.store.write(body), first)
        action = {"type": "probe", "choice": "explain", "revision": 0, "request_id": key()}
        changed = self.store.write(action, first["id"])
        self.assertEqual(self.store.write(action, first["id"]), changed)
        self.assertEqual(len(self.store.list()), 1)
        self.assertEqual(len(self.store.history(first["id"])), 2)
        with self.assertRaises(RehearsalError) as ctx:
            self.store.write({**action, "choice": "rule"}, first["id"])
        self.assertEqual(ctx.exception.status, 409)

    def test_stale_revision_and_invalid_transition_do_not_mutate(self):
        state = self.create()
        changed = self.move(state, "explain")
        for fields in ({"revision": 0}, {"revision": True}, {"type": "transfer"}, {"choice": "unknown"}, {"text": "x"*4001}):
            with self.subTest(fields=fields):
                with self.assertRaises(RehearsalError):
                    self.store.write({"revision": changed["revision"], "type": changed["phase"],
                                      "choice": "tentative", "text": "Lời của người dạy.",
                                      "request_id": key(), **fields}, changed["id"])
                self.assertEqual(self.store.get(state["id"]), changed)
                self.assertEqual(len(self.store.history(state["id"])), 2)

    def test_concurrent_writes_only_one_wins(self):
        state = self.create()
        def write(choice):
            try:
                return self.move(state, choice)["revision"]
            except RehearsalError as error:
                return error.status
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(write, ("explain", "represent")))
        self.assertCountEqual(results, (1, 409))
        self.assertEqual(len(self.store.history(state["id"])), 2)

    def test_unknown_database_and_hardlink_are_preserved(self):
        corpus = Path(self.temp.name) / "knowledge.db"
        with sqlite3.connect(corpus) as conn:
            conn.execute("CREATE TABLE originals(id INTEGER)")
        digest = hashlib.sha256(corpus.read_bytes()).hexdigest()
        hardlink = Path(self.temp.name) / "linked.db"
        os.link(corpus, hardlink)
        for path in (corpus, hardlink):
            with self.assertRaises(ValueError):
                Store(path, self.catalog)
            self.assertEqual(hashlib.sha256(corpus.read_bytes()).hexdigest(), digest)

    def test_symlink_database_is_rejected(self):
        link = Path(self.temp.name) / "symlink.db"
        link.symlink_to(self.path)
        with self.assertRaises(ValueError):
            Store(link, self.catalog)

    def test_pack_change_preserves_read_export_but_blocks_write_replay(self):
        state = self.create()
        pack = json.loads(PACK_PATH.read_text())
        pack["version"] = "changed"
        path = Path(self.temp.name) / "changed.json"
        path.write_text(json.dumps(pack))
        changed = Store(self.path, Catalog(path))
        self.assertEqual(changed.get(state["id"]), state)
        self.assertIn(state["title"], markdown(changed.get(state["id"])))
        with self.assertRaises(RehearsalError):
            changed.write({"revision": 0, "type": "probe", "choice": "rule", "request_id": key()}, state["id"])
        with self.assertRaises(RehearsalError):
            changed.replay(state["id"])

    def test_unicode_free_text_retained_without_semantic_score(self):
        text = '<script>alert("x")</script> Tôi sẽ hỏi: vì sao em chọn như vậy?'
        state = self.move(self.create(), "explain", text)
        self.assertEqual(state["transcript"][1]["text"], text)
        self.assertNotIn("score", state)
        self.assertIn(text, markdown(state))

    def test_empty_reflection_rejected_and_completion_cannot_advance(self):
        state = self.move(self.advance(self.create()), "probe")
        with self.assertRaises(RehearsalError):
            self.move(state, "save", "  ")
        state = self.move(state, "save", "Tôi sẽ kiểm tra bằng một bài khác.")
        with self.assertRaises(RehearsalError):
            self.move(state, "save")

    def test_invalid_create_and_request_ids_are_rejected(self):
        for body in ({"case_id": "missing", "request_id": key()}, {"case_id": [], "request_id": key()},
                     {"case_id": "fraction-magnitude", "request_id": "bad"},
                     {"case_id": "fraction-magnitude", "request_id": key(), "title": False}):
            with self.assertRaises(RehearsalError):
                self.store.write(body)
        self.assertEqual(self.store.list(), [])


if __name__ == "__main__":
    unittest.main()
