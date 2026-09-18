"""Recompute declared keys for the Vietnamese Grade 1 audit profile."""
from datetime import date


def _integer(value, lower=0, upper=100):
    return type(value) is int and lower <= value <= upper


def _list_int(value, size=None):
    return (isinstance(value, list) and (size is None or len(value) == size)
            and all(_integer(v) for v in value))


def check_task(task):
    """Return errors and whether a key was mechanically recomputed.

    Observational rubrics are checked for presence only. Their mathematical,
    visual and pedagogical interpretation remains a human review task.
    """
    if not isinstance(task, dict):
        return ["TASK_SHAPE: expected object"], False
    errors = []
    kind = task.get("kind")
    answer = task.get("answer")
    expected = None
    if not isinstance(task.get("prompt"), str) or not task["prompt"].strip():
        errors.append("TASK_PROMPT: required")
    if kind == "observation":
        if not isinstance(answer, str) or not answer.strip():
            errors.append("OBSERVATION_CRITERION: required")
        return errors, False
    if kind == "arithmetic":
        values, operators = task.get("operands"), task.get("operators")
        if (not _list_int(values) or not isinstance(operators, list)
                or not 1 <= len(operators) <= 2 or len(values) != len(operators) + 1
                or any(op not in ("+", "-") for op in operators)):
            return errors + ["ARITHMETIC_SCOPE: integers 0-100; one/two + or - operators"], False
        expected = values[0]
        for operator, other in zip(operators, values[1:]):
            previous = expected
            expected = previous + other if operator == "+" else previous - other
            if not _integer(expected):
                errors.append("NUMBER_RANGE: every intermediate result must be 0-100")
                break
            # Facts within ten and calculations on whole tens are explicitly
            # included. 6+4 and 100-40 must not be rejected as column algorithms.
            basic_fact = max(previous, other, expected) <= 10
            whole_tens = previous % 10 == 0 and other % 10 == 0
            if not basic_fact and not whole_tens:
                if operator == "+" and previous % 10 + other % 10 >= 10:
                    errors.append("CARRYING: outside this core Grade 1 profile")
                if operator == "-" and previous % 10 < other % 10:
                    errors.append("BORROWING: outside this core Grade 1 profile")
        if not _integer(answer):
            errors.append("ANSWER_TYPE: finite integer required")
    elif kind in ("number", "count"):
        if not _integer(task.get("value")) or not _integer(answer):
            return errors + ["NUMBER_RANGE: integer 0-100 required"], False
        expected = task["value"]
    elif kind == "place":
        if not _integer(task.get("value")) or not _list_int(answer, 2):
            return errors + ["PLACE_SHAPE: integer and [tens, units] required"], False
        expected = [task["value"] // 10, task["value"] % 10]
    elif kind == "compare":
        values = task.get("values")
        if not _list_int(values, 2):
            return errors + ["COMPARE_SHAPE: two integers required"], False
        expected = "<" if values[0] < values[1] else ">" if values[0] > values[1] else "="
    elif kind == "order":
        values = task.get("values")
        if not _list_int(values) or not 2 <= len(values) <= 4:
            return errors + ["ORDER_SCOPE: two to four integers required"], False
        expected = sorted(values)
        if not _list_int(answer, len(values)):
            errors.append("ANSWER_TYPE: ordered integer list required")
    elif kind == "measurement":
        positions = task.get("positions_cm")
        if (not _list_int(positions, 2) or positions[1] < positions[0]
                or task.get("unit") != "cm" or not _integer(answer)):
            return errors + ["MEASURE_SCOPE: cm, ordered endpoints and integer answer required"], False
        expected = positions[1] - positions[0]
    elif kind == "clock":
        if (not _integer(task.get("hour"), 1, 12) or type(task.get("minute")) is not int
                or task["minute"] != 0 or not _integer(answer, 1, 12)):
            return errors + ["CLOCK_SCOPE: whole hours on a 12-hour clock only"], False
        expected = task["hour"]
    elif kind == "calendar":
        try:
            value = date.fromisoformat(task["date"])
        except (ValueError, TypeError, KeyError):
            return errors + ["CALENDAR_DATE: valid ISO date required"], False
        expected = {"weekday": value.weekday(), "day": value.day}
        if (not isinstance(answer, dict) or not _integer(answer.get("weekday"), 0, 6)
                or not _integer(answer.get("day"), 1, 31)):
            errors.append("ANSWER_TYPE: weekday 0-6 and day 1-31 required")
    else:
        return errors + ["TASK_KIND: unsupported; no silent acceptance"], False
    if expected != answer:
        errors.append(f"ANSWER_KEY: declared {answer!r}; recomputed {expected!r}")
    return errors, not errors
