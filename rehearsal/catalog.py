"""Load immutable authored cases and expose only the current task."""

import hashlib
import json
from pathlib import Path

from .errors import RehearsalError

PACK_PATH = Path(__file__).parent / "data" / "fractions.vi.json"


class Catalog:
    def __init__(self, path=PACK_PATH):
        raw = Path(path).read_bytes()
        self.data = json.loads(raw)
        self.fingerprint = hashlib.sha256(raw).hexdigest()
        self.version = self.data["version"]
        self.cases = {c["id"]: c for c in self.data["cases"]}
        if len(self.cases) != len(self.data["cases"]):
            raise ValueError("Duplicate case IDs")
        for case in self.cases.values():
            if case["case_kind"] != "authored_simulation":
                raise ValueError("The rehearsal accepts authored simulation cases only")
            if case["transfer"]["answer"] not in {o["id"] for o in case["transfer"]["options"]}:
                raise ValueError("Transfer answer must reference an option")
            for phase in ("probe", "teach", "check"):
                expected = {o["id"] for o in self.data["prompts"][phase]["options"]}
                if set(case[phase + "_responses"]) != expected:
                    raise ValueError(f"Incomplete {phase} branches: {case['id']}")

    def case(self, identifier):
        if identifier not in self.cases:
            raise RehearsalError("Không tìm thấy tình huống.", "case_not_found", 404)
        return self.cases[identifier]

    def public(self):
        return {"version": self.version, "mode": "authored_rehearsal",
                "notice": self.data["notice"], "review_status": "expert_review_pending",
                "cases": [{k: c[k] for k in ("id", "title", "summary", "stage", "case_kind")}
                          for c in self.cases.values()], "sources": self.data["sources"]}

    def prompt(self, state):
        phase = state["phase"]
        if phase == "complete":
            return None
        if phase == "transfer":
            transfer = self.case(state["case_id"])["transfer"]
            return {k: transfer[k] for k in ("title", "question", "options")}
        return self.data["prompts"][phase]
