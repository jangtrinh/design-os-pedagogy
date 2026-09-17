"""Separate SQLite storage with transactional events and idempotent writes."""

import hashlib
import json
import sqlite3
import uuid
from contextlib import closing, contextmanager
from datetime import datetime, timezone
from pathlib import Path

from . import engine
from .errors import RehearsalError

APPLICATION_ID = 1096045138


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False)


def now():
    return datetime.now(timezone.utc).isoformat()


def request_key(body):
    key = body.get("request_id")
    try:
        if not isinstance(key, str) or str(uuid.UUID(key)) != key:
            raise ValueError
    except ValueError:
        raise RehearsalError("request_id phải là UUID hợp lệ.") from None
    return key, hashlib.sha256(encoded(body).encode()).hexdigest()


class Store:
    def __init__(self, path, catalog):
        self.path, self.catalog = Path(path).absolute(), catalog
        if self.path.is_symlink():
            raise ValueError("Session database must not be a symlink")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.exists():
            with closing(sqlite3.connect(self.path.as_uri() + "?mode=ro", uri=True)) as conn:
                if conn.execute("PRAGMA application_id").fetchone()[0] != APPLICATION_ID:
                    raise ValueError("Existing file is not an Agent Teacher session database")
        with self.connect() as conn:
            conn.execute(f"PRAGMA application_id={APPLICATION_ID}")
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS sessions(id TEXT PRIMARY KEY, snapshot TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS events(
                    session_id TEXT NOT NULL REFERENCES sessions(id), revision INTEGER NOT NULL,
                    event TEXT NOT NULL, at TEXT NOT NULL, PRIMARY KEY(session_id,revision));
                CREATE TABLE IF NOT EXISTS requests(
                    id TEXT PRIMARY KEY, digest TEXT NOT NULL, session_id TEXT NOT NULL REFERENCES sessions(id));
            """)

    @contextmanager
    def connect(self):
        conn = sqlite3.connect(self.path, timeout=5)
        conn.execute("PRAGMA foreign_keys=ON")
        try:
            with conn:
                yield conn
        finally:
            conn.close()

    def _get(self, conn, identifier):
        row = conn.execute("SELECT snapshot FROM sessions WHERE id=?", (identifier,)).fetchone()
        if row is None:
            raise RehearsalError("Không tìm thấy phiên luyện tập.", "session_not_found", 404)
        return json.loads(row[0])

    def get(self, identifier):
        with self.connect() as conn:
            return self._get(conn, identifier)

    def list(self):
        with self.connect() as conn:
            rows = conn.execute("SELECT snapshot FROM sessions ORDER BY rowid DESC LIMIT 100").fetchall()
        return [{k: s[k] for k in ("id", "title", "phase", "revision", "updated_at", "case_id")}
                for s in (json.loads(r[0]) for r in rows)]

    def write(self, body, identifier=None):
        if not isinstance(body, dict):
            raise RehearsalError("Nội dung phải là JSON object.")
        key, digest = request_key({**body, "target_session": identifier})
        with self.connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            previous = conn.execute("SELECT digest,session_id FROM requests WHERE id=?", (key,)).fetchone()
            if previous:
                if digest != previous[0]:
                    raise RehearsalError("request_id đã dùng cho nội dung khác.", "request_conflict", 409)
                return self._get(conn, previous[1])
            at = now()
            if identifier is None:
                allowed = {"case_id", "title", "request_id"}
                if set(body) - allowed or not isinstance(body.get("case_id"), str):
                    raise RehearsalError("Thông tin tạo phiên không hợp lệ.")
                identifier = str(uuid.uuid4())
                event = {"type": "create", "case_id": body["case_id"], "title": body.get("title", "")}
                state = engine.create(event["case_id"], event["title"], identifier, at, self.catalog)
                conn.execute("INSERT INTO sessions VALUES(?,?)", (identifier, encoded(state)))
            else:
                state = self._get(conn, identifier)
                if type(body.get("revision")) is not int or body["revision"] != state["revision"]:
                    raise RehearsalError("Phiên đã thay đổi ở cửa sổ khác. Tải bản mới; bản nháp của bạn vẫn được giữ.",
                                         "revision_conflict", 409)
                if set(body) - {"revision", "request_id", "type", "choice", "text"}:
                    raise RehearsalError("Hành động có trường không được hỗ trợ.")
                event = {k: body[k] for k in ("type", "choice", "text") if k in body}
                state = engine.apply(state, event, at, self.catalog)
                conn.execute("UPDATE sessions SET snapshot=? WHERE id=?", (encoded(state), identifier))
            conn.execute("INSERT INTO events VALUES(?,?,?,?)", (identifier, state["revision"], encoded(event), at))
            conn.execute("INSERT INTO requests VALUES(?,?,?)", (key, digest, identifier))
        return state

    def history(self, identifier):
        with self.connect() as conn:
            self._get(conn, identifier)
            rows = conn.execute("SELECT revision,event,at FROM events WHERE session_id=? ORDER BY revision",
                                (identifier,)).fetchall()
        return [{"revision": r, "event": json.loads(e), "at": t} for r, e, t in rows]

    def replay(self, identifier):
        with self.connect() as conn:
            conn.execute("BEGIN")
            saved = self._get(conn, identifier)
            rows = conn.execute("SELECT revision,event,at FROM events WHERE session_id=? ORDER BY revision",
                                (identifier,)).fetchall()
        events = [{"revision": r, "event": json.loads(e), "at": t} for r, e, t in rows]
        if saved["pack_fingerprint"] != self.catalog.fingerprint:
            raise RehearsalError("Bộ tình huống đã đổi; chưa thể replay bằng phiên bản hiện tại.", "pack_changed", 409)
        first = events[0]
        state = engine.create(first["event"]["case_id"], first["event"]["title"], identifier, first["at"], self.catalog)
        for row in events[1:]:
            state = engine.apply(state, row["event"], row["at"], self.catalog)
        return {"matches_saved_state": state == saved, "event_count": len(events), "revision": saved["revision"]}
