"""Actual course fixture and deliberately corrupted inputs; no simulated pupils."""
import copy
import hashlib
import tempfile
import unittest
from pathlib import Path

from tools.course_support.audit import audit_bundle, load_bundle
from tools.course_support.math_checks import check_task


class CourseAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder = Path(__file__).resolve().parents[1] / "courses/vi-vn-grade-1-math"
        cls.base = load_bundle(cls.folder)

    def setUp(self):
        self.course, self.sessions, self.profile, self.exams, _ = copy.deepcopy(self.base)

    def report(self):
        return audit_bundle(self.course, self.sessions, self.profile, self.exams)

    def rejects(self, marker):
        report = self.report()
        self.assertFalse(report["passed"])
        self.assertTrue(any(marker in e for e in report["errors"]), report["errors"])

    def test_authored_course_passes_only_declared_audit_scope(self):
        report = self.report()
        self.assertTrue(report["passed"], report["errors"])
        self.assertEqual(report["counts"], {"sessions": 105, "outcomes": 24,
                                           "keys_recomputed": 111, "observational_tasks": 14})
        self.assertEqual(report["strands"], {"number": 84, "geometry": 16, "experience": 5})
        self.assertEqual(report["learning_effectiveness"], "not_assessed")
        self.assertEqual(report["learner_pilot"], "not_run")

    def test_missing_solid_requirement_cannot_be_hidden_in_a_polished_course(self):
        for session in self.sessions:
            session["standard_ids"] = [r for r in session["standard_ids"] if r != "R14"]
        self.course["outcomes"] = [o for o in self.course["outcomes"] if "R14" not in o["standard_ids"]]
        self.rejects("COVERAGE")

    def test_deleting_requirement_from_profile_does_not_reduce_target(self):
        self.profile["requirements"] = [r for r in self.profile["requirements"] if r["id"] != "R22"]
        self.rejects("PROFILE_REQUIREMENTS")

    def test_outcomes_need_matching_practice_and_assessment(self):
        self.course["outcomes"][0]["practice_ids"] = ["P999"]
        self.rejects("ALIGNMENT")
        self.course["outcomes"][0]["practice_ids"] = ["P002"]
        self.rejects("ALIGNMENT")

    def test_duplicate_and_missing_periods_fail(self):
        self.sessions[-1] = copy.deepcopy(self.sessions[-2])
        self.rejects("PERIOD_SEQUENCE")
        self.rejects("DUPLICATE_ID")

    def test_time_budget_mismatch_and_hidden_homework_fail(self):
        self.sessions[0]["activity_minutes"][0] += 1
        self.sessions[1]["mandatory_homework_minutes"] = 20
        self.rejects("TIME_BUDGET")
        self.rejects("HIDDEN_HOMEWORK")

    def test_prerequisite_cycle_and_future_dependency_fail(self):
        self.course["units"][0]["prerequisite_unit_ids"] = ["U02"]
        self.rejects("PREREQUISITE_CYCLE")
        self.rejects("PREREQUISITE_ORDER")

    def test_wrong_arithmetic_key_fails(self):
        self.sessions[18]["exit_task"]["answer"] = 99
        self.rejects("ANSWER_KEY")

    def test_borrowing_carrying_and_multiplication_fail(self):
        cases = [([28, 17], ["+"], 45, "CARRYING"),
                 ([52, 8], ["-"], 44, "BORROWING"),
                 ([3, 4], ["*"], 12, "ARITHMETIC_SCOPE")]
        for values, operators, answer, marker in cases:
            with self.subTest(marker=marker):
                task = dict(prompt="Test", kind="arithmetic", operands=values,
                            operators=operators, answer=answer)
                failures, verified = check_task(task)
                self.assertFalse(verified)
                self.assertTrue(any(marker in e for e in failures), failures)

    def test_facts_to_ten_and_whole_tens_remain_allowed(self):
        for values, operator, answer in [([6, 4], "+", 10), ([10, 6], "-", 4),
                                        ([100, 40], "-", 60), ([90, 10], "+", 100)]:
            with self.subTest(values=values):
                self.assertEqual(check_task(dict(prompt="Test", kind="arithmetic", operands=values,
                                                 operators=[operator], answer=answer)), ([], True))

    def test_two_step_order_and_intermediate_range_are_checked(self):
        failures, _ = check_task(dict(prompt="Test", kind="arithmetic", operands=[9, 2, 1],
                                     operators=["-", "+"], answer=6))
        self.assertTrue(any("ANSWER_KEY" in e for e in failures))
        failures, _ = check_task(dict(prompt="Test", kind="arithmetic", operands=[100, 10, 10],
                                     operators=["+", "-"], answer=100))
        self.assertTrue(any("NUMBER_RANGE" in e for e in failures))

    def test_five_number_order_and_half_hour_fail(self):
        self.sessions[15]["exit_task"].update(values=[1, 2, 3, 4, 5], answer=[1, 2, 3, 4, 5])
        self.sessions[91]["exit_task"]["minute"] = 30
        self.rejects("ORDER_SCOPE")
        self.rejects("CLOCK_SCOPE")

    def test_calendar_day_mismatch_fails(self):
        self.sessions[92]["exit_task"]["answer"]["weekday"] = 0
        self.rejects("ANSWER_KEY")

    def test_nonreader_support_and_grade_scope_are_explicit(self):
        self.sessions[0]["reading_required"] = True
        self.course["learner_profile"]["stage"] = "AL2"
        self.rejects("READING_DEPENDENCY")
        self.rejects("LEARNER_SCOPE")

    def test_exam_cannot_assess_before_instruction_or_use_decimal_points(self):
        self.exams["groups"][1]["period"] = 5
        self.exams["groups"][0]["items"][0]["points"] = 0.5
        self.rejects("ASSESSMENT_BEFORE_PRACTICE")
        self.rejects("EXAM_POINTS")

    def test_missing_source_and_fabricated_effectiveness_fail(self):
        self.course["sources"][0]["locator"] = ""
        self.course["review"]["learning_effectiveness"] = "proven"
        self.rejects("SOURCE_LOCATOR")
        self.rejects("EFFECTIVENESS_CLAIM")

    def test_unknown_source_id_fails_with_registry_check(self):
        report = audit_bundle(self.course, self.sessions, self.profile, self.exams, known_sources=set())
        self.assertFalse(report["passed"])
        self.assertTrue(any("UNKNOWN_KNOWLEDGE_SOURCE" in e for e in report["errors"]))

    def test_malformed_shapes_are_diagnostics_not_success(self):
        for value in (None, "wrong", [None]):
            with self.subTest(value=value):
                course = copy.deepcopy(self.course)
                course["outcomes"] = value
                report = audit_bundle(course, self.sessions, self.profile, self.exams)
                self.assertFalse(report["passed"])

    def test_load_and_audit_are_read_only(self):
        def hashes():
            return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in self.folder.glob("*.yaml")}
        before = hashes()
        loaded = load_bundle(self.folder)
        audit_bundle(*loaded[:4])
        self.assertEqual(before, hashes())

    def test_duplicate_yaml_key_and_path_escape_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "course.yaml").write_text("id: a\nid: b\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_bundle(root)
            (root / "course.yaml").write_text("session_files: ['../outside.yaml']\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_bundle(root)


if __name__ == "__main__":
    unittest.main()
