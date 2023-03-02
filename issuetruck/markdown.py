import os
import re
from datetime import date
from io import TextIOWrapper
from pathlib import Path
from typing import Literal

from .issue import Issue, PriorityEnum, StatusEnum, TypeEnum


def parse_path(filepath: Path) -> list[Issue]:
    if not os.path.isfile(filepath):
        return []
    with open(filepath, "r", encoding="utf8") as file:
        return parse_file(file)


def parse_file(file: TextIOWrapper) -> list[Issue]:
    issues: list[Issue] = []
    current = None
    _tdata = False
    _content = False
    for line in file:
        tag = parse_line(line)
        if tag == "h1":
            issue_id, title = parse_h1(line)
            current = Issue(id=issue_id, title=title)
            issues.append(current)
            _tdata = False
            _content = False
        if tag == "h2" and current:
            current.subtitle = parse_h2(line)
        if tag == "tsep":
            _tdata = True
        if tag == "tdata" and _tdata and current:
            parts = parse_tvalues(parse_tdata(line))
            current.status = parts[0]
            current.open_date = parts[1]
            current.done_date = parts[2]
            current.close_date = parts[3]
            current.environment = parts[4]
            current.priority = parts[5]
            current.type = parts[6]
            current.milestone = parts[7]
            _content = True
        if tag in ("empty", "p", "li") and _content and current:
            if stripped := line.strip():
                current.content += stripped + "\n"

    return issues


Tag = Literal["unknown", "empty", "h1", "h2", "h3", "tdata", "tsep", "p", "li"]


def parse_line(line: str) -> Tag:
    if line.startswith("# "):
        return "h1"
    if line.startswith("## "):
        return "h2"
    if line.startswith("### "):
        return "h3"
    if re.match(r"\|\s+-+\s+\|", line):
        return "tsep"
    if re.match(r"\|\s+.*?\s+\|", line):
        return "tdata"
    if line.strip() == "":
        return "empty"
    if re.match(r"^\w+", line):
        return "p"
    if re.match(r"^- ", line):
        return "li"
    return "unknown"


def parse_h1(line: str) -> tuple[int, str]:
    issue_id, title = line[1:].split("-")
    return int(issue_id.strip()), title.strip()


def parse_h2(line: str) -> str:
    return line[2:].strip()


def parse_h3(line: str) -> str:
    return line[3:].strip()


def parse_tdata(line: str) -> list[str]:
    return [item.strip() for item in line[1:-1].split("|")]


def parse_tvalues(
    values: list[str],
) -> tuple[
    StatusEnum, date | None, date | None, date | None, str, PriorityEnum, TypeEnum, str
]:
    return (
        parse_status(values[0]),
        # Open date
        parse_date(values[1]),
        # Done date
        parse_date(values[2]),
        # Close date
        parse_date(values[3]),
        # Environment
        values[4],
        parse_priority(values[5]),
        parse_type(values[6]),
        parse_milestone(values[7]),
    )


def parse_status(status: str) -> StatusEnum:
    return StatusEnum(status.strip())


def parse_priority(status: str) -> PriorityEnum:
    return PriorityEnum(status.strip())


def parse_type(status: str) -> TypeEnum:
    return TypeEnum(status.strip())


def parse_milestone(milestone: str) -> str:
    _milestone = milestone.strip()
    if re.match(r"\d+\.\d+\.\d+", _milestone):
        return _milestone
    return ""


def parse_date(date_value: str) -> date | None:
    parts = date_value.split("/")
    if len(parts) != 3:
        return None
    return date(int(parts[2]), int(parts[1]), int(parts[0]))


def dump_path(filepath: Path, issues: list[Issue]):
    with open(filepath, "w", encoding="utf8") as file:
        for issue in issues:
            print(str(issue), file=file, end="")
