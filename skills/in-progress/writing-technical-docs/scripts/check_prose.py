#!/usr/bin/env python3
"""Report mechanical risks in Markdown technical prose.

This is a heuristic aid, not an ASD-STE100 compliance checker.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


PROMOTIONAL_TERMS = (
    "best-in-class",
    "cutting-edge",
    "effortless",
    "enterprise-grade",
    "game-changing",
    "next-generation",
    "powerful",
    "revolutionary",
    "robust",
    "seamless",
    "state-of-the-art",
    "turnkey",
    "world-class",
)

HEDGE_PHRASES = (
    "as mentioned above",
    "it is important to note",
    "it is worth noting",
    "it should be noted",
    "may potentially",
    "please note that",
)

PHRASAL_VERBS = (
    "circle back",
    "dive into",
    "drill down",
    "kick off",
    "ramp up",
    "reach out",
    "roll out",
    "spin down",
    "spin up",
    "tear down",
)

IRREGULAR_PARTICIPLES = (
    "built",
    "done",
    "found",
    "given",
    "held",
    "kept",
    "known",
    "made",
    "put",
    "read",
    "run",
    "seen",
    "sent",
    "set",
    "shown",
    "taken",
    "written",
)

WORD = re.compile(r"[A-Za-z0-9]+(?:[-'/][A-Za-z0-9]+)*")
SENTENCE_BREAK = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"“])")
CONTRACTION = re.compile(
    r"\b(?:[A-Za-z]+n['’]t|[A-Za-z]+['’](?:d|ll|m|re|ve)|(?:here|it|let|that|there|what|who)['’]s)\b",
    re.IGNORECASE,
)
PASSIVE = re.compile(
    rf"\b(?:am|are|be|been|being|is|was|were)\s+(?:[A-Za-z]+ed|{'|'.join(IRREGULAR_PARTICIPLES)})\b",
    re.IGNORECASE,
)
ING_CONSTRUCTION = re.compile(r"\b(?:am|are|be|been|being|is|was|were)\s+[A-Za-z]+ing\b", re.IGNORECASE)
NOMINALIZATION = re.compile(
    r"\b(?:carry out|conduct|make|perform|provide)(?:s|ed|ing)?\s+(?:a|an|the)?\s*[A-Za-z-]*(?:ance|ence|ment|tion)\b",
    re.IGNORECASE,
)
INLINE_CODE = re.compile(r"`[^`]*`")
QUOTED_TEXT = re.compile(r'"[^"\n]*"|“[^”\n]*”')
MARKDOWN_LINK = re.compile(r"\[([^]]+)]\([^)]*\)")
HTML_TAG = re.compile(r"<[^>]+>")
LIST_PREFIX = re.compile(r"^\s*(?:#{1,6}\s+|[-*+]\s+|\d+[.)]\s+)")
VERSION = re.compile(r"\b[vV]?\d+(?:\.\d+)+\b")
INITIALISM = re.compile(r"\b(?:[A-Za-z]\.){2,}")


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    line: int
    message: str
    excerpt: str


def protect_markdown(lines: list[str]) -> list[tuple[int, str]]:
    """Remove immutable text and join soft-wrapped prose into blocks."""
    output: list[tuple[int, str]] = []
    paragraph: list[str] = []
    paragraph_line = 0
    fence: str | None = None
    frontmatter = bool(lines and lines[0].strip() == "---")

    def flush() -> None:
        nonlocal paragraph, paragraph_line
        if paragraph:
            output.append((paragraph_line, " ".join(paragraph)))
            paragraph = []
            paragraph_line = 0

    for number, raw in enumerate(lines, 1):
        if frontmatter:
            if number > 1 and raw.strip() == "---":
                frontmatter = False
            continue
        stripped = raw.lstrip()
        if fence:
            if stripped.startswith(fence):
                fence = None
            continue
        if stripped.startswith("```") or stripped.startswith("~~~"):
            flush()
            fence = stripped[:3]
            continue
        standalone = bool(LIST_PREFIX.match(raw))
        text = INLINE_CODE.sub(" IMMUTABLE ", raw)
        text = QUOTED_TEXT.sub(" IMMUTABLE ", text)
        text = MARKDOWN_LINK.sub(r"\1", text)
        text = HTML_TAG.sub(" ", text)
        text = VERSION.sub(" VERSION ", text)
        text = INITIALISM.sub(" INITIALISM ", text)
        text = text.replace("**", "").replace("__", "")
        text = LIST_PREFIX.sub("", text).strip()
        if not text:
            flush()
        elif standalone:
            flush()
            output.append((number, text))
        else:
            if not paragraph:
                paragraph_line = number
            paragraph.append(text)
    flush()
    return output


def word_count(text: str) -> int:
    return len(WORD.findall(text))


def excerpt(text: str, limit: int = 120) -> str:
    compact = " ".join(text.split())
    return compact if len(compact) <= limit else compact[: limit - 1] + "…"


def phrase_hits(text: str, phrases: tuple[str, ...]) -> list[str]:
    lowered = text.lower()
    return [phrase for phrase in phrases if re.search(rf"(?<![a-z]){re.escape(phrase)}(?![a-z])", lowered)]


def split_sentences(text: str) -> list[str]:
    return [part.strip() for part in SENTENCE_BREAK.split(text) if part.strip()]


def inspect_line(line_number: int, text: str, max_words: int) -> list[Finding]:
    findings: list[Finding] = []

    for sentence in split_sentences(text):
        count = word_count(sentence)
        if count > max_words:
            findings.append(
                Finding("error", "long-sentence", line_number, f"Sentence has {count} words; limit is {max_words}.", excerpt(sentence))
            )

    if ";" in text:
        findings.append(Finding("error", "semicolon", line_number, "Replace the semicolon with separate sentences.", excerpt(text)))

    if CONTRACTION.search(text):
        findings.append(Finding("warning", "contraction", line_number, "Expand the contraction unless it is immutable text.", excerpt(text)))

    if PASSIVE.search(text):
        findings.append(Finding("warning", "passive-voice", line_number, "Name the actor when it is known.", excerpt(text)))

    if ING_CONSTRUCTION.search(text):
        findings.append(Finding("warning", "ing-construction", line_number, "Use a simple verb form when it preserves the meaning.", excerpt(text)))

    if NOMINALIZATION.search(text):
        findings.append(Finding("warning", "nominalization", line_number, "Use a direct verb for the action.", excerpt(text)))

    for phrase in phrase_hits(text, HEDGE_PHRASES):
        findings.append(Finding("warning", "hedge", line_number, f"Replace vague framing: {phrase!r}.", excerpt(text)))

    for phrase in phrase_hits(text, PHRASAL_VERBS):
        findings.append(Finding("warning", "phrasal-verb", line_number, f"Use a specific verb instead of {phrase!r}.", excerpt(text)))

    for phrase in phrase_hits(text, PROMOTIONAL_TERMS):
        findings.append(Finding("warning", "promotional-term", line_number, f"Replace {phrase!r} with observable behavior or evidence.", excerpt(text)))

    if "—" in text or "–" in text:
        findings.append(Finding("warning", "dash", line_number, "Check whether the dash joins ideas that need separate sentences.", excerpt(text)))

    return findings


def inspect_text(text: str, max_words: int) -> list[Finding]:
    findings: list[Finding] = []
    for line_number, line in protect_markdown(text.splitlines()):
        findings.extend(inspect_line(line_number, line, max_words))
    return findings


def render_text(path: str, findings: list[Finding]) -> str:
    rows = [f"{path}:{item.line}: {item.severity}: {item.code}: {item.message} [{item.excerpt}]" for item in findings]
    errors = sum(item.severity == "error" for item in findings)
    warnings = len(findings) - errors
    rows.append(f"{path}: {errors} error(s), {warnings} warning(s)")
    return "\n".join(rows)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="Markdown or text files. Read stdin when omitted.")
    parser.add_argument("--max-words", type=int, default=25, help="Maximum words per sentence (default: 25).")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.max_words < 1:
        raise SystemExit("--max-words must be positive")

    inputs: list[tuple[str, str]] = []
    if args.paths:
        for value in args.paths:
            path = Path(value)
            inputs.append((str(path), path.read_text(encoding="utf-8")))
    else:
        inputs.append(("<stdin>", sys.stdin.read()))

    reports = []
    error_count = 0
    for name, source in inputs:
        findings = inspect_text(source, args.max_words)
        error_count += sum(item.severity == "error" for item in findings)
        reports.append({"path": name, "findings": [asdict(item) for item in findings]})

    if args.format == "json":
        print(json.dumps(reports, indent=2))
    else:
        print("\n".join(render_text(report["path"], [Finding(**item) for item in report["findings"]]) for report in reports))
    return 1 if error_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
