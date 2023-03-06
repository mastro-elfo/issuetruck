import re
from datetime import date

from issuetruck.issue import (
    Issue,
    PriorityEnum,
    StatusEnum,
    TypeEnum,
    apply_filters,
    filter_by_environment,
    filter_by_milestone,
    filter_by_priority_critical,
    filter_by_priority_high,
    filter_by_priority_low,
    filter_by_priority_medium,
    filter_by_status_canceled,
    filter_by_status_closed,
    filter_by_status_open,
    filter_by_status_test,
    filter_by_title,
    filter_by_type_bug,
    filter_by_type_experimental,
    filter_by_type_feature,
    filter_by_type_improvement,
    filter_by_type_memo,
    format_comment,
    get_by_id,
    get_new_id,
    get_new_priority,
    paginate,
    print_issues,
    split_issues_to_archive,
)


def test_format():
    output_str = str(
        Issue(
            id=1,
            title="Title",
            subtitle="Subtitle",
            status=StatusEnum.OPEN,
            open_date=date(2020, 2, 1),
            done_date=date(2021, 4, 3),
            close_date=date(2022, 6, 5),
            environment="FE",
            priority=PriorityEnum.MEDIUM,
            type=TypeEnum.FEATURE,
            milestone="1.2.3",
        )
    )
    output_parts = output_str.split("\n")
    assert output_parts[0].startswith("# ")
    assert " 1 " in output_parts[0]
    assert "- Title" in output_parts[0]
    assert output_parts[1].startswith("## ")
    assert " Subtitle" in output_parts[1]
    assert re.match(r".*?\|\s+Open\s+\|", output_parts[5])
    assert re.match(r".*?\|\s+01/02/2020\s+\|", output_parts[5])
    assert re.match(r".*?\|\s+03/04/2021\s+\|", output_parts[5])
    assert re.match(r".*?\|\s+05/06/2022\s+\|", output_parts[5])
    assert re.match(r".*?\|\s+FE\s+\|", output_parts[5])
    assert re.match(r".*?\|\s+Medium\s+\|", output_parts[5])
    assert re.match(r".*?\|\s+Feature\s+\|", output_parts[5])
    assert re.match(r".*?\|\s+1.2.3\s+\|", output_parts[5])


def test_filter_by_status_open():
    assert len(filter_by_status_open([], True)) == 0
    assert len(filter_by_status_open(ISSUES, True)) == 2
    assert len(filter_by_status_open(ISSUES, False)) == len(ISSUES)


def test_filter_by_status_closed():
    assert len(filter_by_status_closed([], True)) == 0
    assert len(filter_by_status_closed(ISSUES, True)) == 1
    assert len(filter_by_status_closed(ISSUES, False)) == len(ISSUES)


def test_filter_by_status_test():
    assert len(filter_by_status_test([], True)) == 0
    assert len(filter_by_status_test(ISSUES, True)) == 1
    assert len(filter_by_status_test(ISSUES, False)) == len(ISSUES)


def test_filter_by_status_canceled():
    assert len(filter_by_status_canceled([], True)) == 0
    assert len(filter_by_status_canceled(ISSUES, True)) == 1
    assert len(filter_by_status_canceled(ISSUES, False)) == len(ISSUES)


def test_filter_by_type_bug():
    assert len(filter_by_type_bug([], True)) == 0
    assert len(filter_by_type_bug(ISSUES, True)) == 1
    assert len(filter_by_type_bug(ISSUES, False)) == len(ISSUES)


def test_filter_by_type_feature():
    assert len(filter_by_type_feature([], True)) == 0
    assert len(filter_by_type_feature(ISSUES, True)) == 1
    assert len(filter_by_type_feature(ISSUES, False)) == len(ISSUES)


def test_filter_by_type_improvement():
    assert len(filter_by_type_improvement([], True)) == 0
    assert len(filter_by_type_improvement(ISSUES, True)) == 1
    assert len(filter_by_type_improvement(ISSUES, False)) == len(ISSUES)


def test_filter_by_type_experimental():
    assert len(filter_by_type_experimental([], True)) == 0
    assert len(filter_by_type_experimental(ISSUES, True)) == 1
    assert len(filter_by_type_experimental(ISSUES, False)) == len(ISSUES)


def test_filter_by_type_memo():
    assert len(filter_by_type_memo([], True)) == 0
    assert len(filter_by_type_memo(ISSUES, True)) == 1
    assert len(filter_by_type_memo(ISSUES, False)) == len(ISSUES)


def test_filter_by_priority_medium():
    assert len(filter_by_priority_medium([], True)) == 0
    assert len(filter_by_priority_medium(ISSUES, True)) == 2
    assert len(filter_by_priority_medium(ISSUES, False)) == len(ISSUES)


def test_filter_by_priority_low():
    assert len(filter_by_priority_low([], True)) == 0
    assert len(filter_by_priority_low(ISSUES, True)) == 1
    assert len(filter_by_priority_low(ISSUES, False)) == len(ISSUES)


def test_filter_by_priority_high():
    assert len(filter_by_priority_high([], True)) == 0
    assert len(filter_by_priority_high(ISSUES, True)) == 1
    assert len(filter_by_priority_high(ISSUES, False)) == len(ISSUES)


def test_filter_by_priority_critical():
    assert len(filter_by_priority_critical([], True)) == 0
    assert len(filter_by_priority_critical(ISSUES, True)) == 1
    assert len(filter_by_priority_critical(ISSUES, False)) == len(ISSUES)


def test_filter_by_environment():
    assert len(filter_by_environment([], "DEV")) == 0
    assert len(filter_by_environment(ISSUES, "DEV")) == 1
    assert len(filter_by_environment(ISSUES, None)) == len(ISSUES)


def test_filter_by_milestone():
    assert len(filter_by_milestone([], "1.")) == 0
    assert len(filter_by_milestone(ISSUES, "1.")) == 3
    assert len(filter_by_milestone([], "1.2.")) == 0
    assert len(filter_by_milestone(ISSUES, "1.2.")) == 2
    assert len(filter_by_milestone([], "1.2.3")) == 0
    assert len(filter_by_milestone(ISSUES, "1.2.3")) == 1
    assert len(filter_by_milestone([], "2.")) == 0
    assert len(filter_by_milestone(ISSUES, "2.")) == 1
    assert len(filter_by_milestone(ISSUES, None)) == len(ISSUES)


def test_filter_by_title():
    assert len(filter_by_title([], None)) == 0
    assert len(filter_by_title([], "")) == 0
    assert len(filter_by_title([], "DEF")) == 0
    assert len(filter_by_title([], "ghi")) == 0
    assert len(filter_by_title([], "XYZ")) == 0
    assert len(filter_by_title(ISSUES, None)) == len(ISSUES)
    assert len(filter_by_title(ISSUES, "")) == len(ISSUES)
    assert len(filter_by_title(ISSUES, "DEF")) == 2
    assert len(filter_by_title(ISSUES, "ghi")) == 2
    assert len(filter_by_title(ISSUES, "XYZ")) == 0


def test_apply_filters():
    assert len(apply_filters([])) == 0
    assert len(apply_filters(ISSUES)) == len(ISSUES)

    assert len(apply_filters([], is_open=True)) == 0
    assert len(apply_filters(ISSUES, is_open=True)) == 2
    assert len(apply_filters(ISSUES, is_open=False)) == len(ISSUES)

    assert len(apply_filters([], closed=True)) == 0
    assert len(apply_filters(ISSUES, closed=True)) == 1
    assert len(apply_filters(ISSUES, closed=False)) == len(ISSUES)

    assert len(apply_filters([], test=True)) == 0
    assert len(apply_filters(ISSUES, test=True)) == 1
    assert len(apply_filters(ISSUES, test=False)) == len(ISSUES)

    assert len(apply_filters([], bug=True)) == 0
    assert len(apply_filters(ISSUES, bug=True)) == 1
    assert len(apply_filters(ISSUES, bug=False)) == len(ISSUES)

    assert len(apply_filters([], feature=True)) == 0
    assert len(apply_filters(ISSUES, feature=True)) == 1
    assert len(apply_filters(ISSUES, feature=False)) == len(ISSUES)

    assert len(apply_filters([], improvement=True)) == 0
    assert len(apply_filters(ISSUES, improvement=True)) == 1
    assert len(apply_filters(ISSUES, improvement=False)) == len(ISSUES)

    assert len(apply_filters([], experimental=True)) == 0
    assert len(apply_filters(ISSUES, experimental=True)) == 1
    assert len(apply_filters(ISSUES, experimental=False)) == len(ISSUES)

    assert len(apply_filters([], memo=True)) == 0
    assert len(apply_filters(ISSUES, memo=True)) == 1
    assert len(apply_filters(ISSUES, memo=False)) == len(ISSUES)

    assert len(apply_filters([], low=True)) == 0
    assert len(apply_filters(ISSUES, low=True)) == 1
    assert len(apply_filters(ISSUES, low=False)) == len(ISSUES)

    assert len(apply_filters([], medium=True)) == 0
    assert len(apply_filters(ISSUES, medium=True)) == 2
    assert len(apply_filters(ISSUES, medium=False)) == len(ISSUES)

    assert len(apply_filters([], high=True)) == 0
    assert len(apply_filters(ISSUES, high=True)) == 1
    assert len(apply_filters(ISSUES, high=False)) == len(ISSUES)

    assert len(apply_filters([], critical=True)) == 0
    assert len(apply_filters(ISSUES, critical=True)) == 1
    assert len(apply_filters(ISSUES, critical=False)) == len(ISSUES)

    assert len(apply_filters([], environment="DEV")) == 0
    assert len(apply_filters(ISSUES, environment="DEV")) == 1
    assert len(apply_filters([], milestone="1.")) == 0
    assert len(apply_filters(ISSUES, milestone="1.")) == 3
    assert len(apply_filters([], milestone="1.2.")) == 0
    assert len(apply_filters(ISSUES, milestone="1.2.")) == 2
    assert len(apply_filters([], milestone="1.2.3")) == 0
    assert len(apply_filters(ISSUES, milestone="1.2.3")) == 1
    assert len(apply_filters([], milestone="2.")) == 0
    assert len(apply_filters(ISSUES, milestone="2.")) == 1
    assert len(apply_filters(ISSUES, milestone="2.")) == 1
    assert len(apply_filters(ISSUES, milestone="")) == len(ISSUES)
    assert len(apply_filters(ISSUES, milestone=None)) == len(ISSUES)

    assert len(apply_filters([], title="DEF")) == 0
    assert len(apply_filters(ISSUES, title="DEF")) == 2
    assert len(apply_filters(ISSUES, title="ghi")) == 2
    assert len(apply_filters(ISSUES, title="XYZ")) == 0
    assert len(apply_filters(ISSUES, title="")) == len(ISSUES)
    assert len(apply_filters(ISSUES, title=None)) == len(ISSUES)


def test_get_new_id():
    assert get_new_id(ISSUES) == 6
    assert get_new_id(ISSUES, 3) == 6
    assert get_new_id(ISSUES, 100) == 100
    assert get_new_id([]) == 1
    assert get_new_id([], 3) == 3
    assert get_new_id([], 100) == 100


def test_get_new_priority():
    assert get_new_priority() == PriorityEnum.MEDIUM
    assert get_new_priority(None, None) == PriorityEnum.MEDIUM
    assert get_new_priority(PriorityEnum.CRITICAL) == PriorityEnum.CRITICAL
    assert get_new_priority(PriorityEnum.CRITICAL, None) == PriorityEnum.CRITICAL
    assert (
        get_new_priority(PriorityEnum.CRITICAL, TypeEnum.BUG) == PriorityEnum.CRITICAL
    )
    assert (
        get_new_priority(PriorityEnum.CRITICAL, TypeEnum.IMPROVEMENT)
        == PriorityEnum.CRITICAL
    )
    assert get_new_priority(None, TypeEnum.BUG) == PriorityEnum.MEDIUM
    assert get_new_priority(None, TypeEnum.IMPROVEMENT) == PriorityEnum.LOW


def test_get_by_id():
    issue_1 = get_by_id(ISSUES, 1)
    assert issue_1 is not None
    assert issue_1.id == 1

    issue_4 = get_by_id(ISSUES, 4)
    assert issue_4 is not None
    assert issue_4.id == 4

    issue_100 = get_by_id(ISSUES, 100)
    assert issue_100 is None


def test_print_issues():
    class WriteCount:
        count: int = 0

        def write(self, _: str) -> None:
            self.count += 1

    counter = WriteCount()
    print_issues([], file=counter)
    assert counter.count == 0

    counter = WriteCount()
    print_issues(ISSUES, file=counter)
    assert counter.count > 0


def test_split_issues_to_archive():
    to_archive, to_keep = split_issues_to_archive([])
    assert len(to_archive) == 0
    assert len(to_keep) == 0
    to_archive, to_keep = split_issues_to_archive(ISSUES_TO_ARCHIVE)
    assert len(to_archive) == 1
    assert len(to_keep) == 1
    to_archive, to_keep = split_issues_to_archive(ISSUES_TO_KEEP)
    assert len(to_archive) == 0
    assert len(to_keep) == 2


def test_format_comment():
    assert (
        format_comment(date(2020, 3, 4), "create", "message1", "ENDL")
        == "04/03/2020 - create - message1ENDL"
    )
    assert (
        format_comment(date(2021, 4, 5), "edit", "message2", "ENDL")
        == "05/04/2021 - edit - message2ENDL"
    )
    assert (
        format_comment(date(2022, 5, 6), "status", "message3", "ENDL")
        == "06/05/2022 - status - message3ENDL"
    )


def test_paginate():
    assert len(paginate([])) == 0
    assert len(paginate([], skip=2)) == 0
    assert len(paginate([], limit=3)) == 0
    assert len(paginate([], skip=2, limit=3)) == 0
    assert len(paginate(ISSUES)) == len(ISSUES)
    assert len(paginate(ISSUES, skip=2)) == len(ISSUES) - 2
    assert len(paginate(ISSUES, limit=3)) == 3
    assert len(paginate(ISSUES, skip=2, limit=3)) == 3


ISSUES: list[Issue] = [
    Issue(
        id=1,
        title="ABC DEF",
        status=StatusEnum.OPEN,
        open_date=date(2020, 2, 2),
        type=TypeEnum.BUG,
        priority=PriorityEnum.CRITICAL,
        environment="DEV",
        milestone="1.0.0",
    ),
    Issue(
        id=2,
        title="ABC GHI",
        status=StatusEnum.CLOSED,
        open_date=date(2020, 2, 2),
        type=TypeEnum.FEATURE,
        priority=PriorityEnum.HIGH,
        environment="TEST",
        milestone="1.2.0",
    ),
    Issue(
        id=3,
        title="DEF GHI",
        status=StatusEnum.TEST,
        open_date=date(2020, 2, 2),
        type=TypeEnum.IMPROVEMENT,
        priority=PriorityEnum.LOW,
        environment="COLL",
        milestone="1.2.3",
    ),
    Issue(
        id=4,
        title="JKL",
        status=StatusEnum.CANCELED,
        open_date=date(2020, 2, 2),
        type=TypeEnum.MEMO,
        priority=PriorityEnum.MEDIUM,
        environment="PROD",
        milestone="2.0.0",
    ),
    Issue(
        id=5,
        title="JKL",
        status=StatusEnum.OPEN,
        open_date=date(2020, 2, 2),
        type=TypeEnum.EXPERIMENTAL,
        priority=PriorityEnum.MEDIUM,
        environment="PROD",
        milestone="3.0.0",
    ),
]

ISSUES_TO_ARCHIVE: list[Issue] = [
    Issue(
        id=2,
        title="",
        status=StatusEnum.CLOSED,
        open_date=date(2020, 2, 2),
        type=TypeEnum.FEATURE,
        priority=PriorityEnum.HIGH,
        environment="TEST",
        milestone="1.2.0",
    ),
    Issue(
        id=4,
        title="",
        status=StatusEnum.CANCELED,
        open_date=date(2020, 2, 2),
        type=TypeEnum.IMPROVEMENT,
        priority=PriorityEnum.MEDIUM,
        environment="PROD",
        milestone="2.0.0",
    ),
]

ISSUES_TO_KEEP: list[Issue] = [
    Issue(
        id=1,
        title="",
        status=StatusEnum.OPEN,
        open_date=date(2020, 2, 2),
        type=TypeEnum.BUG,
        priority=PriorityEnum.CRITICAL,
        environment="DEV",
        milestone="1.0.0",
    ),
    Issue(
        id=3,
        title="",
        status=StatusEnum.TEST,
        open_date=date(2020, 2, 2),
        type=TypeEnum.IMPROVEMENT,
        priority=PriorityEnum.LOW,
        environment="COLL",
        milestone="1.2.3",
    ),
]
