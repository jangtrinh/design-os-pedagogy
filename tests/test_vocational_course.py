"""Vocational course fixture: real schedule, replanning scenarios and corrupted inputs."""
import copy
import unittest
from pathlib import Path

from tools.course_support.vocational.audit import audit, schedule_digest
from tools.course_support.vocational.model import load_bundle, to_minutes
from tools.course_support.vocational.planner import diff, plan

FOLDER = Path(__file__).resolve().parents[1] / "courses/vi-vn-tvet-plc-logo-zen"
SCHEDULE = "schedules/cd9-k5-2026.yaml"
SESSIONS = "sessions/cd9-k5-2026.yaml"


def document(schedule, result):
    return {"sessions_version": "tvet-sessions-1.0", "schedule_sha256": schedule_digest(schedule),
            "unscheduled": result["unscheduled"], "sessions": result["sessions"]}


class VocationalCourseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = load_bundle(FOLDER, SCHEDULE, SESSIONS)

    def setUp(self):
        self.course, self.schedule, self.sessions, _ = copy.deepcopy(self.base)

    def replan(self, *exceptions):
        self.schedule["exceptions"] = list(exceptions)
        result = plan(self.course, self.schedule)
        return result, audit(self.course, self.schedule, document(self.schedule, result))

    def rejects(self, marker, sessions=None):
        report = audit(self.course, self.schedule, self.sessions if sessions is None else sessions)
        self.assertFalse(report["passed"])
        self.assertTrue(any(marker in e for e in report["errors"]), report["errors"])

    # Baseline -----------------------------------------------------------------

    def test_committed_plan_passes_and_keeps_honesty_fields(self):
        report = audit(self.course, self.schedule, self.sessions)
        self.assertTrue(report["passed"], report["errors"])
        self.assertEqual(report["counts"]["sessions"], 15)
        self.assertEqual((report["counts"]["theory_hours"], report["counts"]["practice_hours"],
                          report["counts"]["exam_hours"]), (14.0, 42.0, 4.0))
        self.assertEqual(report["learning_effectiveness"], "not_assessed")
        self.assertEqual(report["teacher_review"], "not_run")
        self.assertTrue(any(w.startswith("PROGRAM_DEVIATION: B5") for w in report["warnings"]))

    def test_planner_reproduces_committed_plan_exactly(self):
        result = plan(self.course, self.schedule)
        self.assertEqual(result["sessions"], self.sessions["sessions"])
        self.assertEqual(result["unscheduled"], [])

    def test_session_minutes_follow_45_60_rule(self):
        by_id = {s["id"]: s for s in self.sessions["sessions"]}
        total = lambda s: sum(p["minutes"] for p in s["phases"])
        self.assertEqual(total(by_id["W01"]), 2 * 45 + 2 * 60)
        self.assertEqual(total(by_id["W08"]), 240)
        self.assertEqual([p["kind"] for p in by_id["W15"]["phases"]], ["kiem_tra"])
        self.assertIn("kiem_tra", [p["kind"] for p in by_id["W10"]["phases"]])

    # Replanning ---------------------------------------------------------------

    def test_cancelled_week_with_make_up_session_passes(self):
        result, report = self.replan(
            {"kind": "cancel_session", "week": 6, "reason": "Nghỉ đột xuất"},
            {"kind": "add_session", "start": "2026-12-05", "hours": 4, "reason": "Học bù"})
        self.assertTrue(report["passed"], report["errors"])
        changes = diff(self.sessions["sessions"], result["sessions"])
        self.assertEqual(changes["removed"], ["W06"])
        self.assertEqual(changes["added"], ["M01"])
        final = [s for s in result["sessions"] if any(b.get("assessment_id") == "THI-KT" for b in s["blocks"])]
        self.assertEqual([s["id"] for s in final], ["W15"])

    def test_lost_week_without_make_up_is_reported_not_hidden(self):
        result, report = self.replan({"kind": "cancel_session", "week": 6, "reason": "Nghỉ đột xuất"})
        self.assertFalse(report["passed"])
        self.assertTrue(any(e.startswith("UNSCHEDULED") for e in report["errors"]))
        self.assertEqual(sum(to_minutes(b["hours"]) for b in result["unscheduled"]), 240)

    def test_shortened_session_moves_only_later_sessions(self):
        result, _ = self.replan({"kind": "set_hours", "week": 8, "hours": 3, "reason": "Họp khoa"})
        changes = diff(self.sessions["sessions"], result["sessions"])
        self.assertTrue(changes["changed"])
        self.assertTrue(all(c >= "W08" for c in changes["changed"]))

    def test_missing_kit_does_not_receive_zen_lessons(self):
        result, _ = self.replan({"kind": "equipment_unavailable", "week": 11, "equipment_ids": ["zen-kit"],
                                 "reason": "Kit hỏng"})
        self.assertNotIn("W11", [s["id"] for s in result["sessions"]])

    def test_extended_lesson_stays_before_dependent_and_assessment(self):
        result, report = self.replan(
            {"kind": "extend_lesson", "lesson_id": "B4", "block_kind": "practice", "hours": 2, "reason": "Lớp chậm"},
            {"kind": "add_session", "start": "2026-12-12", "hours": 2, "reason": "Học bù"})
        self.assertTrue(report["passed"], report["errors"])

    # Corrupted inputs ---------------------------------------------------------

    def test_editing_schedule_without_replanning_is_stale(self):
        self.schedule["weeks"][0]["blocks"][0]["items"].append("1.3")
        self.rejects("STALE_PLAN")

    def test_phase_minutes_must_match_session_length(self):
        self.sessions["sessions"][2]["phases"][3]["minutes"] += 5
        self.rejects("PHASE_MINUTES")

    def test_phase_kinds_are_closed_and_ordered(self):
        phases = self.sessions["sessions"][2]["phases"]
        phases[0], phases[-1] = phases[-1], phases[0]
        self.rejects("PHASE_ORDER")

    def test_assessment_cannot_precede_its_scope(self):
        first, tenth = self.sessions["sessions"][0], self.sessions["sessions"][9]
        test = tenth["blocks"].pop()
        first["blocks"].insert(0, test)
        self.rejects("ASSESSED_BEFORE_TAUGHT")

    def test_dependent_lesson_cannot_start_first(self):
        self.course["lessons"][1]["prerequisite_ids"] = ["B3"]
        self.rejects("PREREQUISITE_ORDER")

    def test_prerequisite_cycle_is_rejected(self):
        self.course["lessons"][0]["prerequisite_ids"] = ["B2"]
        self.rejects("PREREQUISITE_CYCLE")

    def test_zen_lesson_in_logo_only_week_is_rejected_at_baseline(self):
        self.schedule["weeks"][10]["equipment_ids"] = ["pc", "projector", "logo-soft", "logo-kit"]
        self.rejects("SCHEDULE_EQUIPMENT")

    def test_module_hours_must_match_program(self):
        self.course["module_program"]["practice_hours"] = 46
        self.rejects("MODULE_HOURS")

    def test_lab_without_safety_or_rubric_is_rejected(self):
        self.course["labs"][2]["safety"] = []
        self.course["labs"][3]["rubric"] = self.course["labs"][3]["rubric"][:2]
        report = audit(self.course, self.schedule, self.sessions)
        self.assertTrue(any("LAB_SAFETY" in e for e in report["errors"]))
        self.assertTrue(any("LAB_RUBRIC" in e for e in report["errors"]))

    def test_inferred_solution_cannot_be_marked_verified_without_verifier(self):
        lab = next(l for l in self.course["labs"] if l["solution_basis"] == "inferred")
        lab["verification"] = "teacher_verified"
        self.rejects("LAB_VERIFIER")

    def test_practice_lesson_needs_a_task(self):
        self.course["lessons"][0]["lab_ids"] = []
        self.course["labs"] = [l for l in self.course["labs"] if l["lesson_id"] != "B1"]
        self.rejects("PRACTICE_WITHOUT_TASK")

    def test_effectiveness_claim_is_rejected(self):
        self.course["review"]["learning_effectiveness"] = "improved"
        self.rejects("EFFECTIVENESS_CLAIM")

    def test_ga_numbers_and_previous_lesson_follow_order(self):
        self.sessions["sessions"][4]["ga_number"] = 9
        self.sessions["sessions"][5]["previous_lesson_id"] = "B1"
        report = audit(self.course, self.schedule, self.sessions)
        self.assertTrue(any("GA_NUMBER" in e for e in report["errors"]))
        self.assertTrue(any("PREVIOUS_LESSON" in e for e in report["errors"]))

    def test_planner_rejects_unknown_exception_and_off_grid_hours(self):
        self.schedule["exceptions"] = [{"kind": "teleport", "week": 3, "reason": "x"}]
        with self.assertRaises(ValueError):
            plan(self.course, self.schedule)
        self.schedule["exceptions"] = [{"kind": "set_hours", "week": 3, "hours": 3.1, "reason": "x"}]
        with self.assertRaises(ValueError):
            plan(self.course, self.schedule)


if __name__ == "__main__":
    unittest.main()
