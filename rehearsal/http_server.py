"""Loopback HTTP interface with strict request and asset boundaries."""

import json
import logging
import re
import sqlite3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlsplit

from .errors import RehearsalError
from .exporter import markdown

MAX_BODY = 32 * 1024
SESSION = re.compile(r"^/api/sessions/([a-f0-9-]{36})(?:/(events|replay|export))?$")
ASSETS = {"/": ("index.html", "text/html"), "/app.js": ("app.js", "text/javascript"),
          "/views.js": ("views.js", "text/javascript"), "/styles.css": ("styles.css", "text/css")}


def object_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON property")
        result[key] = value
    return result


def make_handler(store, catalog, static_root):
    root = static_root.resolve()

    class Handler(BaseHTTPRequestHandler):
        def setup(self):
            super().setup()
            self.connection.settimeout(10)

        def log_message(self, *args):
            pass

        def reply(self, status, payload, mime="application/json", filename=None):
            if mime == "application/json":
                payload = json.dumps(payload, ensure_ascii=False, allow_nan=False).encode("utf-8")
            elif isinstance(payload, str):
                payload = payload.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", mime + "; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'")
            if filename:
                self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
            self.end_headers()
            self.wfile.write(payload)

        def guard(self):
            port = self.server.server_address[1]
            hosts = {f"localhost:{port}", f"127.0.0.1:{port}"}
            if self.headers.get("Host") not in hosts:
                raise RehearsalError("Chỉ nhận yêu cầu từ địa chỉ cục bộ.", "forbidden", 403)
            if self.headers.get("Origin") not in (None, *("http://" + h for h in hosts)):
                raise RehearsalError("Yêu cầu khác nguồn bị từ chối.", "forbidden", 403)
            if self.headers.get("Sec-Fetch-Site") == "cross-site":
                raise RehearsalError("Yêu cầu khác nguồn bị từ chối.", "forbidden", 403)

        def body(self):
            if self.headers.get_content_type() != "application/json" or self.headers.get("Transfer-Encoding"):
                raise RehearsalError("Hãy gửi JSON với Content-Length hợp lệ.")
            lengths = self.headers.get_all("Content-Length", [])
            if len(lengths) != 1 or not lengths[0].isdigit():
                raise RehearsalError("Content-Length không hợp lệ.")
            length = int(lengths[0])
            if not 0 < length <= MAX_BODY:
                raise RehearsalError("Yêu cầu vượt quá 32 KB hoặc rỗng.", "body_limit", 413)
            try:
                body = json.loads(self.rfile.read(length), object_pairs_hook=object_pairs,
                                  parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
                if not isinstance(body, dict):
                    raise ValueError
                return body
            except (ValueError, UnicodeError, RecursionError, TimeoutError):
                raise RehearsalError("Nội dung JSON không hợp lệ.") from None

        def dispatch(self):
            self.guard()
            parsed = urlsplit(self.path)
            path = unquote(parsed.path)
            if self.command == "GET" and path in ASSETS:
                name, mime = ASSETS[path]
                asset = root / name
                if asset.is_symlink() or not asset.is_file() or asset.resolve().parent != root:
                    raise RehearsalError("Thiếu tài nguyên giao diện.", "asset_missing", 503)
                return self.reply(200, asset.read_bytes(), mime)
            if path == "/api/status" and self.command == "GET":
                return self.reply(200, {"mode": "authored_rehearsal", "model_calls": False,
                                       "pack_version": catalog.version, "expert_review": "pending"})
            if path == "/api/catalog" and self.command == "GET":
                return self.reply(200, catalog.public())
            if path == "/api/sessions":
                if self.command == "GET":
                    return self.reply(200, {"items": store.list()})
                if self.command == "POST":
                    return self.reply(201, {"session": store.write(self.body())})
            match = SESSION.fullmatch(path)
            if match:
                identifier, action = match.groups()
                if self.command == "POST" and action == "events":
                    return self.reply(200, {"session": store.write(self.body(), identifier)})
                if self.command == "GET":
                    if action == "events":
                        return self.reply(200, {"items": store.history(identifier)})
                    if action == "replay":
                        return self.reply(200, store.replay(identifier))
                    state = store.get(identifier)
                    if action == "export":
                        format = parse_qs(parsed.query).get("format", ["md"])[0]
                        if format not in ("md", "json"):
                            raise RehearsalError("Chỉ hỗ trợ Markdown hoặc JSON.")
                        return self.reply(200, markdown(state) if format == "md" else state,
                                          "text/markdown" if format == "md" else "application/json",
                                          f"rehearsal-{identifier}.{format}")
                    return self.reply(200, {"session": state})
            raise RehearsalError("Không tìm thấy nội dung.", "not_found", 404)

        def run_request(self):
            try:
                self.dispatch()
            except RehearsalError as error:
                self.reply(error.status, {"error": {"code": error.code, "message": str(error)}})
            except sqlite3.Error:
                self.reply(503, {"error": {"code": "storage_unavailable", "message": "Chưa lưu được phiên. Bản nháp vẫn được giữ; hãy thử lại."}})
            except (BrokenPipeError, ConnectionResetError, TimeoutError):
                pass
            except Exception:
                logging.exception("Rehearsal request failed")
                self.reply(500, {"error": {"code": "internal_error", "message": "Không hoàn tất được yêu cầu."}})

        do_GET = do_POST = run_request

    return Handler


def create_server(store, catalog, static_root, port=0):
    server = ThreadingHTTPServer(("127.0.0.1", port), make_handler(store, catalog, static_root))
    server.daemon_threads = True
    return server
