from datetime import date
from pathlib import Path
from typing import Optional

import typer

from . import __version__
from .issue import (
    Issue,
    PriorityEnum,
    StatusEnum,
    TypeEnum,
    apply_filters,
    format_comment,
    get_by_id,
    get_new_id,
    get_new_priority,
    print_issues,
    split_issues_to_archive,
)
from .markdown import dump_path, parse_path

DEFAULT_PATH = Path(".") / "ToDo.md"


def version_callback(
    value: Optional[bool] = typer.Option(None, "--version", is_eager=True)
):
    if value:
        print(f"IssueTruck Version: {__version__}")
        raise typer.Exit()


app = typer.Typer(invoke_without_command=True, callback=version_callback)


@app.command("create")
def create_issue_cmd(
    title: str,
    priority: PriorityEnum = typer.Option(None),
    issue_type: TypeEnum = typer.Option(TypeEnum.BUG, "--type"),
    subtitle: str = "",
    environment: str = "",
    milestone: str = "",
    comment: str = "",
    filepath: Path = typer.Option(DEFAULT_PATH),
    start: int = 1,
):
    issues: list[Issue] = parse_path(filepath)
    new_id = get_new_id(issues, start)
    new_priority = get_new_priority(priority, issue_type)
    new_issue = Issue(
        id=new_id,
        title=title,
        status=StatusEnum.OPEN,
        priority=new_priority,
        type=issue_type,
        open_date=date.today(),
        subtitle=subtitle,
        environment=environment,
        milestone=milestone,
        content=format_comment(date.today(), "create", comment, "\n\n")
        if comment
        else "",
    )
    issues.insert(0, new_issue)
    dump_path(filepath, issues)
    print("Created new issue")
    print(f"{new_issue.id} - {new_issue.title}")


@app.command("edit")
def edit_issue_cmd(
    issue_id: int,
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    status: Optional[StatusEnum] = None,
    environment: Optional[str] = None,
    priority: Optional[PriorityEnum] = None,
    issue_type: Optional[TypeEnum] = typer.Option(None, "--type"),
    milestone: Optional[str] = None,
    comment: str = "",
    filepath: Path = typer.Option(DEFAULT_PATH),
):
    issues: list[Issue] = parse_path(filepath)
    issue = get_by_id(issues, issue_id)
    if issue is None:
        print(f"No issue found with id = {issue_id}")
        return
    if status == StatusEnum.TEST and issue.status != StatusEnum.TEST:
        issue.done_date = date.today()
    if status == StatusEnum.CLOSED and issue.status != StatusEnum.CLOSED:
        issue.close_date = date.today()
    if status == StatusEnum.CANCELED and issue.status != StatusEnum.CANCELED:
        issue.close_date = date.today()
    if status == StatusEnum.OPEN:
        issue.done_date = None
        issue.close_date = None
    if title is not None:
        issue.title = title
    if subtitle is not None:
        issue.subtitle = subtitle
    if status is not None:
        issue.status = status
    if environment is not None:
        issue.environment = environment
    if priority is not None:
        issue.priority = priority
    if issue_type is not None:
        issue.type = issue_type
    if milestone is not None:
        issue.milestone = milestone
    if comment:
        issue.content += format_comment(date.today(), "edit", comment, "\n\n")
    dump_path(filepath, issues)
    print(f"Modified issue with id = {issue_id}")


@app.command("list")
def list_issue_cmd(
    is_open: bool = typer.Option(False, "--open"),
    closed: bool = typer.Option(False, "--closed"),
    test: bool = typer.Option(False, "--test"),
    canc: bool = typer.Option(False, "--canceled"),
    bug: bool = typer.Option(False, "--bug"),
    feat: bool = typer.Option(False, "--feat"),
    imp: bool = typer.Option(False, "--imp"),
    low: bool = typer.Option(False, "--low"),
    med: bool = typer.Option(False, "--med"),
    high: bool = typer.Option(False, "--high"),
    crit: bool = typer.Option(False, "--crit"),
    env: Optional[str] = None,
    mil: Optional[str] = None,
    tit: Optional[str] = None,
    filepath: Path = typer.Option(DEFAULT_PATH),
):
    issues: list[Issue] = parse_path(filepath)
    filtered_issues = apply_filters(
        issues,
        is_open=is_open,
        closed=closed,
        test=test,
        canceled=canc,
        bug=bug,
        feature=feat,
        improvement=imp,
        low=low,
        medium=med,
        high=high,
        critical=crit,
        environment=env,
        milestone=mil,
        title=tit,
    )
    print(f"Filter result {len(filtered_issues)}/{len(issues)}")
    print("")
    print_issues(filtered_issues)


@app.command("status")
def change_status(
    issue_id: int,
    is_open: bool = typer.Option(False, "--open"),
    done: bool = typer.Option(False, "--done"),
    close: bool = typer.Option(False, "--close"),
    cancel: bool = typer.Option(False, "--cancel"),
    comment: str = "",
    filepath: Path = typer.Option(DEFAULT_PATH),
):
    issues: list[Issue] = parse_path(filepath)
    issue = get_by_id(issues, issue_id)
    if issue is None:
        print(f"No issue found with id = {issue_id}")
        return
    if is_open and issue.status != StatusEnum.OPEN:
        issue.status = StatusEnum.OPEN
        issue.close_date = None
        issue.done_date = None
    if done and issue.status != StatusEnum.TEST:
        issue.status = StatusEnum.TEST
        issue.done_date = date.today()
    if close and issue.status != StatusEnum.CLOSED:
        issue.status = StatusEnum.CLOSED
        issue.close_date = date.today()
    if cancel and issue.status != StatusEnum.CANCELED:
        issue.status = StatusEnum.CANCELED
        issue.close_date = date.today()
    if comment:
        issue.content += format_comment(date.today(), "status", comment, "\n\n")
    dump_path(filepath, issues)
    print(f"Status set for issue with id = {issue_id}")


@app.command("archive")
def archive(
    filepath: Path = typer.Option(DEFAULT_PATH),
):
    issues: list[Issue] = parse_path(filepath)
    to_archive, to_keep = split_issues_to_archive(issues)
    if not to_archive:
        print("No issue to archive in current main file")
        return

    typer.confirm(
        f"Confirm to apply the following changes: Archive {len(to_archive)}, Keep {len(to_keep)}",
        abort=True,
    )
    today = date.today()
    archive_file_path = Path(".") / f"ToDo-{today:%Y-%m-%d}.md"
    archived_issues = parse_path(archive_file_path)
    dump_path(archive_file_path, to_archive + archived_issues)
    dump_path(filepath, to_keep)
