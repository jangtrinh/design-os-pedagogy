"""Authored content checks and the two site editions; the student edition must not leak teacher material."""
import copy
import re
import tempfile
import unittest
from pathlib import Path

from tools.course_support.vocational.content import check_content, load_content
from tools.course_support.vocational.model import load_bundle
from tools.course_support.vocational.site import Site
from tools.render_course_site import STUDENT_OUT, write

FOLDER = Path(__file__).resolve().parents[1] / "courses/vi-vn-tvet-plc-logo-zen"


class VocationalSiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        course, schedule, sessions, hashes = load_bundle(FOLDER, "schedules/cd9-k5-2026.yaml",
                                                         "sessions/cd9-k5-2026.yaml")
        cls.base = (course, schedule, sessions, load_content(FOLDER, hashes))

    def setUp(self):
        self.course, self.schedule, self.sessions, self.content = copy.deepcopy(self.base)

    def errors(self):
        return check_content(self.course, self.sessions, self.content)

    def rejects(self, marker):
        errors = self.errors()
        self.assertTrue(any(marker in e for e in errors), errors)

    def site(self, audience):
        base = "../../assets/site.css" if audience == "student" else "assets/site.css"
        return Site(self.course, self.schedule, self.sessions, self.content, audience, base).build()

    # Authored content ----------------------------------------------------------

    def test_authored_pilot_content_passes(self):
        self.assertEqual(self.errors(), [])
        self.assertEqual(sorted(self.content["lessons"]), ["B1", "B2", "B3"])
        self.assertEqual(sorted(self.content["sessions"]), ["W01", "W02", "W03"])
        self.assertGreaterEqual(len(self.content["glossary"]["terms"]), 40)

    def test_lesson_plan_must_follow_planned_minutes(self):
        self.content["sessions"]["W01"]["phases"][3]["minutes"] += 5
        self.rejects("GA_PHASES")

    def test_steps_must_fill_the_problem_solving_phase(self):
        phase = next(p for p in self.content["sessions"]["W02"]["phases"] if p["kind"] == "giai_quyet_van_de")
        phase["steps"][0]["minutes"] += 1
        self.rejects("GA_STEP_MINUTES")

    def test_practice_session_needs_a_lab_task(self):
        phase = next(p for p in self.content["sessions"]["W03"]["phases"] if p["kind"] == "giai_quyet_van_de")
        for step in phase["steps"]:
            step.pop("lab_id", None)
        self.rejects("GA_PRACTICE")

    def test_passive_student_column_is_rejected(self):
        self.content["sessions"]["W01"]["phases"][1]["student"] = ["Lắng nghe, ghi nhận."]
        self.rejects("PASSIVE_STUDENT")

    def test_mcq_needs_valid_answer_and_feedback_per_option(self):
        check = self.content["lessons"]["B1"]["sections"][0]["checks"][0]
        check["answer"] = len(check["options"])
        check["feedback"] = check["feedback"][:-1]
        self.rejects("MCQ_ANSWER")
        self.rejects("MCQ_FEEDBACK")

    def test_completion_example_needs_a_blank_step(self):
        example = next(x for x in self.content["lessons"]["B2"]["worked_examples"] if x["fading"] == "completion")
        for step in example["steps"]:
            step.pop("blank", None)
        self.rejects("FADING")

    def test_widget_references_are_checked(self):
        section = next(s for s in self.content["lessons"]["B2"]["sections"] if s.get("widget"))
        section["widget"]["spec"]["outputs"][0]["from"] = "B999"
        self.rejects("WIDGET_REF")

    def test_draft_solution_cannot_be_copied_into_student_brief(self):
        practice = self.content["lessons"]["B3"]["practice"]
        practice["steps"].append(next(l for l in self.course["labs"] if l["id"] == practice["lab_id"])["solution_outline"])
        self.rejects("SOLUTION_LEAK")

    def test_raw_html_in_markdown_is_rejected(self):
        self.content["lessons"]["B1"]["sections"][0]["body_md"] += "\n\n<script>alert(1)</script>"
        self.rejects("SECTION_BODY")

    # Site editions -----------------------------------------------------------

    def test_student_edition_has_no_teacher_material(self):
        pages = self.site("student")
        html = "\n".join(pages.values())
        self.assertFalse(any("giao-an" in name for name in pages))
        self.assertNotIn('<p class="c-callout-title">Chỉ giáo viên</p>', html)
        for lab in self.course["labs"]:
            if lab.get("solution_outline"):
                self.assertNotIn(lab["solution_outline"][:50].replace("&", "&amp;"), html, lab["id"])
            for issue in lab.get("open_issues", []):
                self.assertNotIn(issue[:50].replace("&", "&amp;"), html, lab["id"])
        for doc in self.content["sessions"].values():
            for note in doc.get("teacher_notes", []):
                self.assertNotIn(note[:50].replace("&", "&amp;"), html)
        self.assertNotIn('name="robots"', pages["index.html"])

    def test_teacher_edition_adds_a_lesson_plan_per_session(self):
        pages = self.site("teacher")
        plans = [n for n in pages if n.endswith("-giao-an.html")]
        self.assertEqual(len(plans), len(self.sessions["sessions"]))
        self.assertIn("GIÁO ÁN SỐ: 1", pages["tuan/W01-giao-an.html"])
        self.assertIn('<p class="c-callout-title">Chỉ giáo viên</p>', pages["bai/B3.html"])
        self.assertIn('name="robots" content="noindex"', pages["index.html"])

    def test_every_question_is_rendered_once(self):
        pages = self.site("student")
        for lid, doc in self.content["lessons"].items():
            expected = sum(len(s.get("checks", [])) for s in doc["sections"]) + len(doc["self_test"])
            self.assertEqual(pages[f"bai/{lid}.html"].count('class="c-mcq"'), expected, lid)

    def test_markdown_is_escaped_not_executed(self):
        self.content["lessons"]["B1"]["sections"][0]["body_md"] = "Thử <b>đậm</b> & **thật**"
        page = self.site("student")["bai/B1.html"]
        self.assertIn("&lt;b&gt;", page)
        self.assertIn("<strong>thật</strong>", page)

    def test_internal_links_resolve(self):
        pages = self.site("teacher")
        for name, html in pages.items():
            base = Path(name).parent
            for href in re.findall(r'href="([^"#:]+\.html)', html):
                target = (base / href).as_posix()
                parts = []
                for part in target.split("/"):
                    if part == "..":
                        parts.pop()
                    elif part != ".":
                        parts.append(part)
                self.assertIn("/".join(parts), pages, f"{name} -> {href}")

    def test_committed_student_site_matches_generator(self):
        pages = self.site("student")
        with tempfile.TemporaryDirectory() as tmp:
            write(pages, tmp, "student")
            for name, html in pages.items():
                committed = STUDENT_OUT / name
                self.assertTrue(committed.is_file(), name)
                self.assertEqual(committed.read_text(encoding="utf-8"), html, f"{name} is stale; rerun the build")


if __name__ == "__main__":
    unittest.main()
