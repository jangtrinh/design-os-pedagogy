"""Export observed rehearsal actions; never include unrevealed case keys."""


def markdown(state):
    lines = ["# " + state["title"], "", "Tình huống mô phỏng biên soạn; chưa chứng nhận năng lực.",
             "", f"Phiên bản bộ bài: {state['pack_version']}", f"Trạng thái: {state['phase']}",
             "", "## Diễn biến", ""]
    labels = {"teacher": "Người dạy", "learner": "Học sinh mô phỏng", "coach": "Gợi ý biên soạn"}
    for turn in state["transcript"]:
        lines.extend([f"### {labels[turn['role']]}", "", turn["text"], ""])
    if state["review"]:
        lines.extend(["## Phản hồi theo lựa chọn", ""])
        for item in state["review"]["observations"]:
            lines.extend([item["observation"], ""])
        lines.extend([state["review"]["limit"], ""])
    if state["transfer_feedback"]:
        lines.extend(["## Bài chuyển giao", "", state["transfer_feedback"]["explanation"], ""])
    lines.extend(["## Điều sẽ thay đổi", "", state["reflection"] or "Chưa ghi.", "", "## Nguồn tham khảo", ""])
    for source in state["sources"]:
        lines.extend([source["title"], source["url"], source["scope"], ""])
    return "\n".join(lines)
