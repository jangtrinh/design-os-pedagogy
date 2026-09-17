"""Pure, replayable transitions; feedback describes choices, not latent mastery."""

from copy import deepcopy

from .errors import RehearsalError

PHASES = ("probe", "interpret", "teach", "check", "review", "transfer", "reflect", "complete")


def text_value(value, field, limit=4000):
    if not isinstance(value, str) or len(value) > limit:
        raise RehearsalError(f"{field} phải là văn bản, tối đa {limit} ký tự.")
    return value.strip()


def create(case_id, title, identifier, at, catalog):
    case = catalog.case(case_id)
    state = {"id": identifier, "revision": 0, "case_id": case_id,
             "title": text_value(title, "Tên phiên", 160) or case["title"],
             "created_at": at, "updated_at": at, "pack_version": catalog.version,
             "pack_fingerprint": catalog.fingerprint, "mode": "authored_rehearsal",
             "phase": "probe", "choices": {}, "review": [], "transfer_feedback": None,
             "reflection": "", "case_kind": "authored_simulation",
             "review_status": "expert_review_pending", "sources": deepcopy(catalog.data["sources"]),
             "scenario": {k: case[k] for k in ("title", "context", "observation", "fractions")},
             "transcript": [{"role": "learner", "kind": "initial", "text": case["observation"]}]}
    state["prompt"] = deepcopy(catalog.prompt(state))
    return state


def review(state, case):
    choices = state["choices"]
    observations = []
    messages = {
        "probe": {"explain": "Bạn đã hỏi cách lập luận trước khi chọn cách dạy.",
                  "represent": "Bạn đã yêu cầu biểu diễn để có thêm dấu hiệu quan sát.",
                  "rule": "Nhắc lại quy tắc chưa phân biệt được hiểu bản chất và nhớ lời giải."},
        "interpret": {"tentative": "Bạn giữ cách giải thích như một giả thuyết cần kiểm tra.",
                      "certain": "Kết luận chắc chắn từ một phản hồi có thể bỏ qua nguyên nhân khác.",
                      "insufficient": "Bạn ghi nhận giới hạn bằng chứng; hãy nêu câu hỏi cần thêm."},
        "teach": {"number_line": "Bạn dùng cùng một đơn vị trên trục số để so sánh độ lớn.",
                  "worked_example": "Bạn làm mẫu một ví dụ khác rồi dành bước tiếp theo cho người học.",
                  "rule_only": "Quy tắc ngắn có thể hỗ trợ nhớ; vẫn cần kiểm tra lập luận trên bài khác."},
        "check": {"novel_reason": "Bạn yêu cầu bài mới kèm lý do, thay vì chỉ xác nhận đáp án.",
                  "repeat": "Lặp bài vừa dạy chỉ cho thấy thực hiện lại; chưa kiểm tra chuyển giao.",
                  "praise": "Lời động viên chưa cung cấp bằng chứng người học áp dụng được cách hiểu."}}
    for phase in ("probe", "interpret", "teach", "check"):
        index = next(i for i, turn in enumerate(state["transcript"])
                     if turn["role"] == "teacher" and turn["kind"] == phase)
        observations.append({"phase": phase, "turn_index": index,
                             "quote": state["transcript"][index]["text"],
                             "observation": messages[phase][choices[phase]],
                             "kind": "authored_feedback"})
    return {"observations": observations, "case_note": case["debrief"],
            "next_try": case["alternative"],
            "limit": "Phản hồi dựa trên các lựa chọn đã ghi. Câu chữ tự viết chưa được chấm tự động; chưa chứng nhận năng lực dạy học."}


def apply(state, event, at, catalog):
    if state["pack_fingerprint"] != catalog.fingerprint:
        raise RehearsalError("Bộ tình huống đã đổi. Xuất phiên cũ và tạo phiên mới để tiếp tục.",
                             "pack_changed", 409)
    phase = state["phase"]
    if phase == "complete" or event.get("type") != phase:
        raise RehearsalError("Hành động không phù hợp bước hiện tại.", "invalid_transition", 409)
    choice = event.get("choice")
    options = {o["id"]: o["label"] for o in state["prompt"]["options"]}
    if not isinstance(choice, str) or choice not in options:
        raise RehearsalError("Hãy chọn một phương án trong bước hiện tại.")
    message = text_value(event.get("text", ""), "Lời bạn viết")
    if phase == "reflect" and not message:
        raise RehearsalError("Hãy ghi một điều bạn sẽ thay đổi ở lần dạy tiếp theo.")
    item, case = deepcopy(state), catalog.case(state["case_id"])
    item["choices"][phase] = choice
    item["transcript"].append({"role": "teacher", "kind": phase,
                                "choice": choice, "text": message or options[choice]})
    if phase in ("probe", "teach", "check"):
        response = case[phase + "_responses"][choice]
        if isinstance(response, dict):
            response = response[item["choices"]["teach"]]
        item["transcript"].append({"role": "learner", "kind": phase,
                                    "text": response})
    if phase == "interpret":
        item["transcript"].append({"role": "coach", "kind": phase,
                                    "text": "Giữ giả thuyết này để đối chiếu với phản hồi tiếp theo; chưa kết luận năng lực của người học."})
    if phase == "check":
        item["review"] = review(item, case)
    if phase == "transfer":
        transfer = case["transfer"]
        item["transfer_feedback"] = {"matched_authored_key": choice == transfer["answer"],
                                      "explanation": transfer["feedback"],
                                      "kind": "authored_practice_feedback",
                                      "limit": "Một câu luyện tập không xác nhận mức thành thạo hay hiệu quả của Agent Teacher."}
    if phase == "reflect":
        item["reflection"] = message
    item["phase"] = PHASES[PHASES.index(phase) + 1]
    item["revision"] += 1
    item["updated_at"] = at
    item["prompt"] = deepcopy(catalog.prompt(item))
    return item
