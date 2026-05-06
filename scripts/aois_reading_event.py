#!/usr/bin/env python3
"""Record paragraph-level AOIS reading, link, and question events."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


EVENT_TYPES = {"view", "click", "question"}
HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def repo_root() -> Path:
    try:
        root = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        return Path(root).resolve()
    except (OSError, subprocess.CalledProcessError):
        return Path(__file__).resolve().parents[1]


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def normalize_space(value: str) -> str:
    return " ".join(value.split())


def resolve_repo_file(root: Path, file_value: str) -> tuple[Path, str]:
    path = Path(file_value)
    if not path.is_absolute():
        path = root / path
    path = path.resolve()
    try:
        rel = path.relative_to(root)
    except ValueError as exc:
        raise SystemExit(f"file must be inside repo: {file_value}") from exc
    if not path.is_file():
        raise SystemExit(f"file does not exist: {rel.as_posix()}")
    return path, rel.as_posix()


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def find_line_by_quote(lines: list[str], quote: str | None) -> int | None:
    if not quote:
        return None
    compact_quote = normalize_space(quote)
    for index, line in enumerate(lines, start=1):
        if quote in line or compact_quote in normalize_space(line):
            return index

    full_text = "\n".join(lines)
    position = full_text.find(quote)
    if position < 0:
        position = normalize_space(full_text).find(compact_quote)
    if position < 0:
        return None
    return full_text[:position].count("\n") + 1


def heading_for_line(lines: list[str], line_number: int) -> tuple[str, int] | tuple[None, None]:
    heading = None
    heading_line = None
    for index, line in enumerate(lines[:line_number], start=1):
        match = HEADING_RE.match(line)
        if match:
            heading = normalize_space(match.group(2))
            heading_line = index
    return heading, heading_line


def is_boundary(line: str) -> bool:
    return not line.strip() or HEADING_RE.match(line) is not None


def nearest_content_index(lines: list[str], line_number: int) -> int:
    if not lines:
        return 0
    index = max(0, min(line_number - 1, len(lines) - 1))
    if lines[index].strip():
        return index

    for cursor in range(index - 1, -1, -1):
        if lines[cursor].strip():
            return cursor
    for cursor in range(index + 1, len(lines)):
        if lines[cursor].strip():
            return cursor
    return index


def paragraph_for_line(lines: list[str], line_number: int) -> dict[str, Any]:
    if not lines:
        return {
            "start_line": 1,
            "end_line": 1,
            "index": None,
            "type": "empty",
            "text": "",
            "excerpt": "",
            "links": [],
        }

    index = nearest_content_index(lines, line_number)
    line = lines[index]
    if HEADING_RE.match(line):
        start = end = index
        block_type = "heading"
    else:
        start = index
        while start > 0 and not is_boundary(lines[start - 1]):
            start -= 1
        end = index
        while end + 1 < len(lines) and not is_boundary(lines[end + 1]):
            end += 1
        block_type = "paragraph"

    text = "\n".join(lines[start : end + 1]).strip()
    paragraph_index = 0
    cursor = 0
    while cursor < len(lines):
        if not lines[cursor].strip() or HEADING_RE.match(lines[cursor]):
            cursor += 1
            continue
        paragraph_index += 1
        block_start = cursor
        while cursor + 1 < len(lines) and not is_boundary(lines[cursor + 1]):
            cursor += 1
        block_end = cursor
        if block_start == start and block_end == end:
            break
        cursor += 1
    else:
        paragraph_index = None

    links = [
        {"text": normalize_space(match.group(1)), "href": match.group(2)}
        for match in LINK_RE.finditer(text)
    ]

    return {
        "start_line": start + 1,
        "end_line": end + 1,
        "index": paragraph_index,
        "type": block_type,
        "text": text,
        "excerpt": normalize_space(text)[:500],
        "links": links,
    }


def infer_active_version(rel_file: str) -> str:
    parts = Path(rel_file).parts
    if len(parts) >= 3 and parts[0] == "curriculum":
        if parts[2].startswith("v") or parts[2] in {"00-phase-start", "zz-phase-end"}:
            return f"{parts[1]}/{parts[2]}"
    return "unspecified"


def write_latest_position(root: Path, record: dict[str, Any]) -> None:
    state_dir = root / ".aois-state"
    state_dir.mkdir(parents=True, exist_ok=True)
    latest = state_dir / "latest-reading-position.md"
    paragraph = record["paragraph"]
    paragraph_label = "unspecified"
    if paragraph["index"] is not None:
        paragraph_label = f"{paragraph['index']} (lines {paragraph['start_line']}-{paragraph['end_line']})"

    lines = [
        "# AOIS Reading Position",
        "",
        f"- Timestamp: {record['timestamp']}",
        f"- Event: {record['event_type']}",
        f"- File: {record['file']}",
        f"- Source line: {record['line']}",
        f"- Heading: {record.get('heading') or 'unspecified'}",
        f"- Paragraph: {paragraph_label}",
        f"- Active version: {record['active_version']}",
    ]
    if record.get("href"):
        lines.append(f"- Link clicked: {record['href']}")
    if record.get("link_text"):
        lines.append(f"- Link text: {record['link_text']}")
    lines.extend(["", "## Source Paragraph", "", paragraph["text"] or paragraph["excerpt"]])
    if record.get("question"):
        lines.extend(["", "## Question", "", record["question"]])
    latest.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def append_event(root: Path, record: dict[str, Any]) -> None:
    state_dir = root / ".aois-state"
    state_dir.mkdir(parents=True, exist_ok=True)
    events_file = state_dir / "reader-events.jsonl"
    with events_file.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=True, sort_keys=True) + "\n")
    write_latest_position(root, record)


def run_checkpoint(root: Path, record: dict[str, Any]) -> None:
    checkpoint = root / "scripts" / "aois_checkpoint.sh"
    if not checkpoint.exists():
        return
    paragraph = record["paragraph"]
    location = f"{record['file']}:{paragraph['start_line']}"
    next_step = f"Resume at {location}"
    if record["event_type"] == "click" and record.get("href"):
        next_step = f"Resume from clicked link {record['href']} at {location}"
    if record["event_type"] == "question":
        next_step = f"Answer or continue from question source at {location}"
    note = f"Latest reader event: {record['event_type']} at {location}"
    subprocess.run(
        [
            str(checkpoint),
            "--source",
            f"reader-{record['event_type']}",
            "--lesson",
            record["active_version"],
            "--next",
            next_step,
            "--note",
            note,
        ],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def record_event(
    event_type: str,
    file_value: str,
    *,
    line: int | None = None,
    quote: str | None = None,
    href: str | None = None,
    link_text: str | None = None,
    question: str | None = None,
    checkpoint: bool = True,
) -> dict[str, Any]:
    if event_type not in EVENT_TYPES:
        raise ValueError(f"unsupported event type: {event_type}")

    root = repo_root()
    path, rel_file = resolve_repo_file(root, file_value)
    lines = read_lines(path)
    source_line = line or find_line_by_quote(lines, quote) or 1
    source_line = max(1, min(source_line, max(len(lines), 1)))
    heading, heading_line = heading_for_line(lines, source_line)
    paragraph = paragraph_for_line(lines, source_line)
    record = {
        "timestamp": utc_timestamp(),
        "event_type": event_type,
        "file": rel_file,
        "line": source_line,
        "quote": quote,
        "heading": heading,
        "heading_line": heading_line,
        "paragraph": paragraph,
        "active_version": infer_active_version(rel_file),
        "href": href,
        "link_text": link_text,
        "question": question,
    }
    append_event(root, record)
    if checkpoint:
        run_checkpoint(root, record)
    return record


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="event_type", required=True)

    for event_type in sorted(EVENT_TYPES):
        subparser = subparsers.add_parser(event_type)
        subparser.add_argument("--file", required=True, help="Repo-relative source file")
        subparser.add_argument("--line", type=int, help="Source line in the file")
        subparser.add_argument("--quote", help="Source quote used to find the paragraph")
        subparser.add_argument("--no-checkpoint", action="store_true")
        if event_type == "click":
            subparser.add_argument("--href", required=True, help="Clicked link target")
            subparser.add_argument("--link-text", help="Clicked link text")
        else:
            subparser.add_argument("--href", help=argparse.SUPPRESS)
            subparser.add_argument("--link-text", help=argparse.SUPPRESS)
        if event_type == "question":
            subparser.add_argument("--question", required=True, help="Question text")
        else:
            subparser.add_argument("--question", help=argparse.SUPPRESS)

    latest = subparsers.add_parser("latest")
    latest.set_defaults(event_type="latest")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    root = repo_root()
    if args.event_type == "latest":
        latest_file = root / ".aois-state" / "latest-reading-position.md"
        if not latest_file.exists():
            print(f"No latest reading position found at {latest_file}", file=sys.stderr)
            return 1
        print(latest_file.read_text(encoding="utf-8"), end="")
        return 0

    record = record_event(
        args.event_type,
        args.file,
        line=args.line,
        quote=args.quote,
        href=getattr(args, "href", None),
        link_text=getattr(args, "link_text", None),
        question=getattr(args, "question", None),
        checkpoint=not args.no_checkpoint,
    )
    print(json.dumps(record, ensure_ascii=True, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
