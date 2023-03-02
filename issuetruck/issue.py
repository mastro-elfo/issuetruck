from dataclasses import dataclass
from datetime import date
from enum import Enum
from functools import partial
from typing import TYPE_CHECKING, Literal, Optional

from .compose import compose

if TYPE_CHECKING:  # pragma: no cover
    from _typeshed import SupportsWrite


class StatusEnum(str, Enum):
    OPEN = "Open"
    TEST = "Test"
    CLOSED = "Closed"
    CANCELED = "Canceled"


class PriorityEnum(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class TypeEnum(str, Enum):
    BUG = "Bug"
    FEATURE = "Feature"
    IMPROVEMENT = "Improvement"


@dataclass
class Issue:
    id: int
    title: str
    open_date: Optional[date] = None
    status: StatusEnum = StatusEnum.OPEN
    type: TypeEnum = TypeEnum.BUG
    priority: PriorityEnum = PriorityEnum.MEDIUM
    subtitle: str = ""
    environment: str = ""
    milestone: str = ""
    done_date: Optional[date] = None
    close_date: Optional[date] = None
    content: str = ""

    def __str__(self) -> str:
        return "\n".join(
            x
            for x in [
                self._md_title,
                self._md_subtitle or None,
                "",
                self._md_thead,
                self._md_tsep,
                self._md_tdata,
                "",
                self._md_content or None,
                "" if not self._md_content else None,
            ]
            if x is not None
        )

    @property
    def _md_title(self) -> str:
        return f"# {self.id} - {self.title}"

    @property
    def _md_subtitle(self) -> str:
        return f"## {self.subtitle}" if self.subtitle else ""

    @property
    def _md_thead(self) -> str:
        return "|  Status  | Open date  | Done date  | Close date | Environment | Priority |    Type     |  Milestone  |"

    @property
    def _md_tsep(self) -> str:
        return "| -------- | ---------- | ---------- | ---------- | ----------- | -------- | ----------- | ----------- |"

    @property
    def _md_status(self) -> str:
        return self.status.value

    @property
    def _md_priority(self) -> str:
        return self.priority.value

    @property
    def _md_type(self) -> str:
        return self.type.value

    @property
    def _md_open_date(self) -> str:
        return (
            f"{self.open_date.day:02}/{self.open_date.month:02}/{self.open_date.year:04}"
            if self.open_date
            else ""
        )

    @property
    def _md_done_date(self) -> str:
        return (
            f"{self.done_date.day:02}/{self.done_date.month:02}/{self.done_date.year:04}"
            if self.done_date
            else ""
        )

    @property
    def _md_close_date(self) -> str:
        return (
            f"{self.close_date.day:02}/{self.close_date.month:02}/{self.close_date.year:04}"
            if self.close_date
            else ""
        )

    @property
    def _md_environment(self) -> str:
        return self.environment[:11]

    @property
    def _md_tdata(self) -> str:
        return f"| {self._md_status:<8} | {self._md_open_date} | {self._md_done_date:<10} | {self._md_close_date:<10} | {self._md_environment:<11} | {self._md_priority:<8} | {self._md_type:<11} | {self.milestone:<11} |"

    @property
    def _md_content(self) -> str:
        return self.content


def get_new_id(issues: list[Issue], start: int = 1) -> int:
    if len(issues) == 0:
        return start
    return max(start, max(issue.id for issue in issues) + 1)


def get_new_priority(
    priority_from_cli: Optional[PriorityEnum] = None,
    type_from_cli: Optional[TypeEnum] = None,
) -> PriorityEnum:
    if priority_from_cli is not None:
        return priority_from_cli
    if type_from_cli == TypeEnum.IMPROVEMENT:
        return PriorityEnum.LOW
    return PriorityEnum.MEDIUM


def get_by_id(issues: list[Issue], issue_id: int) -> Issue | None:
    try:
        index = [issue.id for issue in issues].index(issue_id)
    except ValueError:
        return None
    else:
        return issues[index]


def filter_by_status_open(issues: list[Issue], is_open: bool) -> list[Issue]:
    return (
        [issue for issue in issues if issue.status == StatusEnum.OPEN]
        if is_open
        else issues
    )


def filter_by_status_closed(issues: list[Issue], closed: bool) -> list[Issue]:
    return (
        [issue for issue in issues if issue.status == StatusEnum.CLOSED]
        if closed
        else issues
    )


def filter_by_status_test(issues: list[Issue], test: bool) -> list[Issue]:
    return (
        [issue for issue in issues if issue.status == StatusEnum.TEST]
        if test
        else issues
    )


def filter_by_status_canceled(issues: list[Issue], canceled: bool) -> list[Issue]:
    return (
        [issue for issue in issues if issue.status == StatusEnum.CANCELED]
        if canceled
        else issues
    )


def filter_by_type_bug(issues: list[Issue], bug: bool) -> list[Issue]:
    return [issue for issue in issues if issue.type == TypeEnum.BUG] if bug else issues


def filter_by_type_feature(issues: list[Issue], feature: bool) -> list[Issue]:
    return (
        [issue for issue in issues if issue.type == TypeEnum.FEATURE]
        if feature
        else issues
    )


def filter_by_type_improvement(issues: list[Issue], improvement: bool) -> list[Issue]:
    return (
        [issue for issue in issues if issue.type == TypeEnum.IMPROVEMENT]
        if improvement
        else issues
    )


def filter_by_priority_low(issues: list[Issue], low: bool) -> list[Issue]:
    return (
        [issue for issue in issues if issue.priority == PriorityEnum.LOW]
        if low
        else issues
    )


def filter_by_priority_medium(issues: list[Issue], medium: bool) -> list[Issue]:
    return (
        [issue for issue in issues if issue.priority == PriorityEnum.MEDIUM]
        if medium
        else issues
    )


def filter_by_priority_high(issues: list[Issue], high: bool) -> list[Issue]:
    return (
        [issue for issue in issues if issue.priority == PriorityEnum.HIGH]
        if high
        else issues
    )


def filter_by_priority_critical(issues: list[Issue], critical: bool) -> list[Issue]:
    return (
        [issue for issue in issues if issue.priority == PriorityEnum.CRITICAL]
        if critical
        else issues
    )


def filter_by_environment(
    issues: list[Issue], environment: Optional[str]
) -> list[Issue]:
    return (
        [issue for issue in issues if issue.environment == environment]
        if environment
        else issues
    )


def filter_by_milestone(issues: list[Issue], milestone: Optional[str]) -> list[Issue]:
    return (
        [issue for issue in issues if issue.milestone.startswith(milestone)]
        if milestone
        else issues
    )


def filter_by_title(issues: list[Issue], title: Optional[str]) -> list[Issue]:
    return (
        [issue for issue in issues if title.lower() in issue.title.lower()]
        if title
        else issues
    )


def split_issues_to_archive(issues: list[Issue]) -> tuple[list[Issue], list[Issue]]:
    STATUS_TO_ARCHIVE = (StatusEnum.CLOSED, StatusEnum.CANCELED)
    max_id = max(issue.id for issue in issues) if issues else 0

    def archive_condition(issue: Issue):
        return issue.status in STATUS_TO_ARCHIVE and issue.id != max_id

    return (
        [issue for issue in issues if archive_condition(issue)],
        [issue for issue in issues if not archive_condition(issue)],
    )


def apply_filters(
    issues: list[Issue],
    is_open: bool = False,
    closed: bool = False,
    test: bool = False,
    canceled: bool = False,
    bug: bool = False,
    feature: bool = False,
    improvement: bool = False,
    low: bool = False,
    medium: bool = False,
    high: bool = False,
    critical: bool = False,
    environment: Optional[str] = None,
    milestone: Optional[str] = None,
    title: Optional[str] = None,
) -> list[Issue]:
    return compose(
        partial(filter_by_status_open, is_open=is_open),
        partial(filter_by_status_closed, closed=closed),
        partial(filter_by_status_test, test=test),
        partial(filter_by_status_canceled, canceled=canceled),
        partial(filter_by_type_bug, bug=bug),
        partial(filter_by_type_feature, feature=feature),
        partial(filter_by_type_improvement, improvement=improvement),
        partial(filter_by_priority_low, low=low),
        partial(filter_by_priority_medium, medium=medium),
        partial(filter_by_priority_high, high=high),
        partial(filter_by_priority_critical, critical=critical),
        partial(filter_by_environment, environment=environment),
        partial(filter_by_milestone, milestone=milestone),
        partial(filter_by_title, title=title),
    )(issues)


def print_issues(issues: list[Issue], file: "SupportsWrite[str] | None" = None) -> None:
    for issue in issues:
        print(issue, file=file)


def format_comment(
    today: date,
    operation: Literal["create", "edit", "status"],
    message: str,
    end: str = "",
):
    return f"{today.day:02}/{today.month:02}/{today.year:04} - {operation} - {message}{end}"
