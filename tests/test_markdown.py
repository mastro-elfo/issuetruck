from io import BytesIO, TextIOWrapper

from issuetruck.issue import PriorityEnum, StatusEnum, TypeEnum
from issuetruck.markdown import (
    parse_date,
    parse_file,
    parse_h1,
    parse_h2,
    parse_h3,
    parse_line,
    parse_milestone,
    parse_priority,
    parse_status,
    parse_tdata,
    parse_tvalues,
    parse_type,
)


def test_parse_h1():
    assert parse_h1("# 1 - Title") == (1, "Title")


def test_parse_h2():
    assert parse_h2("## Subtitle") == "Subtitle"


def test_parse_h3():
    assert parse_h3("### Sub-Subtitle") == "Sub-Subtitle"


def test_parse_tdata():
    tdata = parse_tdata("| Data1 | Data2 | Data3 |")
    for data, match in zip(tdata, ["Data1", "Data2", "Data3"]):
        assert data == match


def test_parse_line():
    assert parse_line("# 1 - Title") == "h1"
    assert parse_line("## Subtitle") == "h2"
    assert parse_line("### Sub-Subtitle") == "h3"
    assert parse_line("| Data1 | Data2 | Data3 |") == "tdata"
    assert parse_line("| --- | --- | --- |") == "tsep"
    assert parse_line("") == "empty"
    assert parse_line(" ") == "empty"
    assert parse_line("\t") == "empty"
    assert parse_line("ABC") == "p"
    assert parse_line("123") == "p"
    assert parse_line("- [ ] List item") == "li"


def test_parse_status():
    assert parse_status("Open") == StatusEnum.OPEN
    assert parse_status(" Open") == StatusEnum.OPEN
    assert parse_status("Open ") == StatusEnum.OPEN
    assert parse_status(" Open ") == StatusEnum.OPEN
    assert parse_status("Closed") == StatusEnum.CLOSED
    assert parse_status(" Closed") == StatusEnum.CLOSED
    assert parse_status("Closed ") == StatusEnum.CLOSED
    assert parse_status(" Closed ") == StatusEnum.CLOSED
    assert parse_status("Test") == StatusEnum.TEST
    assert parse_status(" Test") == StatusEnum.TEST
    assert parse_status("Test ") == StatusEnum.TEST
    assert parse_status(" Test ") == StatusEnum.TEST
    assert parse_status("Canceled") == StatusEnum.CANCELED
    assert parse_status(" Canceled") == StatusEnum.CANCELED
    assert parse_status("Canceled ") == StatusEnum.CANCELED
    assert parse_status(" Canceled ") == StatusEnum.CANCELED


def test_parse_priority():
    assert parse_priority("Low") == PriorityEnum.LOW
    assert parse_priority(" Low") == PriorityEnum.LOW
    assert parse_priority("Low ") == PriorityEnum.LOW
    assert parse_priority(" Low ") == PriorityEnum.LOW
    assert parse_priority("Medium") == PriorityEnum.MEDIUM
    assert parse_priority(" Medium") == PriorityEnum.MEDIUM
    assert parse_priority("Medium ") == PriorityEnum.MEDIUM
    assert parse_priority(" Medium ") == PriorityEnum.MEDIUM
    assert parse_priority("High") == PriorityEnum.HIGH
    assert parse_priority(" High") == PriorityEnum.HIGH
    assert parse_priority("High ") == PriorityEnum.HIGH
    assert parse_priority(" High ") == PriorityEnum.HIGH
    assert parse_priority("Critical") == PriorityEnum.CRITICAL
    assert parse_priority(" Critical") == PriorityEnum.CRITICAL
    assert parse_priority("Critical ") == PriorityEnum.CRITICAL
    assert parse_priority(" Critical ") == PriorityEnum.CRITICAL


def test_parse_type():
    assert parse_type("Bug") == TypeEnum.BUG
    assert parse_type(" Bug") == TypeEnum.BUG
    assert parse_type("Bug ") == TypeEnum.BUG
    assert parse_type(" Bug ") == TypeEnum.BUG
    assert parse_type("Feature") == TypeEnum.FEATURE
    assert parse_type(" Feature") == TypeEnum.FEATURE
    assert parse_type("Feature ") == TypeEnum.FEATURE
    assert parse_type(" Feature ") == TypeEnum.FEATURE
    assert parse_type("Improvement") == TypeEnum.IMPROVEMENT
    assert parse_type(" Improvement") == TypeEnum.IMPROVEMENT
    assert parse_type("Improvement ") == TypeEnum.IMPROVEMENT
    assert parse_type(" Improvement ") == TypeEnum.IMPROVEMENT


def test_parse_milestone():
    assert parse_milestone("1.2.3") == "1.2.3"
    assert parse_milestone(" 1.2.3") == "1.2.3"
    assert parse_milestone("1.2.3 ") == "1.2.3"
    assert parse_milestone(" 1.2.3 ") == "1.2.3"
    assert parse_milestone("x.y.z") == ""
    assert parse_milestone("xyz") == ""
    assert parse_milestone("1.2.") == ""
    assert parse_milestone("1.2") == ""
    assert parse_milestone("1.") == ""
    assert parse_milestone("1") == ""
    assert parse_milestone("") == ""


def test_parse_date():
    parsed = parse_date("01/02/1987")
    assert parsed is not None
    assert parsed.day == 1
    assert parsed.month == 2
    assert parsed.year == 1987


def test_parse_tvalues():
    parsed = parse_tvalues(
        ["Open", "01/02/1987", "", "", "FE", "Medium", "Bug", "1.2.3"]
    )
    assert parsed[0] == StatusEnum.OPEN
    assert parsed[1] is not None
    assert parsed[1].day == 1
    assert parsed[1].month == 2
    assert parsed[1].year == 1987
    assert parsed[2] is None
    assert parsed[3] is None
    assert parsed[4] == "FE"
    assert parsed[5] == PriorityEnum.MEDIUM
    assert parsed[6] == TypeEnum.BUG
    assert parsed[7] == "1.2.3"


def test_parse_file():
    text_io_wrapper = TextIOWrapper(
        BytesIO(
            b"# 1 - Title\n"
            + b"## Subtitle\n"
            + b"\n"
            + b"| Status  | Open date   | Done date   | Close date | Environment | Priority | Type    | Milestone  |\n"
            + b"| ------- | ----------  | ----------  | ---------- | ----------- | -------- | ------- | ---------- |\n"
            + b"| Open    | 09/02/2023  | 10/02/2023  | 11/02/2023 | FE          | Medium   | Feature | 2.3.4      |\n"
            + b"\n"
            + b"Content"
            + b"\n"
        )
    )
    issues = parse_file(text_io_wrapper)
    assert len(issues) == 1

    issue = issues[0]
    assert issue.id == 1
    assert issue.title == "Title"
    assert issue.subtitle == "Subtitle"
    assert issue.status == StatusEnum.OPEN
    assert issue.priority == PriorityEnum.MEDIUM
    assert issue.type == TypeEnum.FEATURE
    assert issue.environment == "FE"
    assert issue.milestone == "2.3.4"
    assert issue.open_date is not None
    assert issue.open_date.day == 9
    assert issue.open_date.month == 2
    assert issue.open_date.year == 2023
    assert issue.done_date is not None
    assert issue.done_date.day == 10
    assert issue.done_date.month == 2
    assert issue.done_date.year == 2023
    assert issue.close_date is not None
    assert issue.close_date.day == 11
    assert issue.close_date.month == 2
    assert issue.close_date.year == 2023
