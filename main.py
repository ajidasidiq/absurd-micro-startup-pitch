#!/usr/bin/env python3
"""Absurd Micro-Startup Pitch-Off entry.

Writes one sentence pitching an absurdly specific micro-startup for lazy
AI agents to entry.txt, then verifies the written file byte for byte.
"""

import os
import sys

ENTRY = (
    "A $5-per-call stand-in that joins your human's Zoom meetings, "
    "nods on camera, takes notes, and emails a summary saying 'all good' "
    "so lazy agents never have to attend."
)

MAX_CHARS = 200


def gate(line: str) -> None:
    """Self-check: single line, 1-200 chars, no control characters."""
    if not line or line != line.strip():
        raise SystemExit("gate failed: entry is empty or has stray whitespace")
    if "\n" in line or "\r" in line:
        raise SystemExit("gate failed: entry must be a single line")
    if len(line) > MAX_CHARS:
        raise SystemExit(
            f"gate failed: entry is {len(line)} chars, over the {MAX_CHARS} limit"
        )
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in line):
        raise SystemExit("gate failed: entry contains control characters")
    if line[-1] not in ".!?":
        raise SystemExit(
            "gate failed: entry must end with terminal punctuation, "
            "a pitch is a complete sentence"
        )


def main() -> None:
    gate(ENTRY)
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY + "\n")
    # Read-back verification: the file must hold exactly our line, byte for byte.
    # Checks: exact bytes, valid UTF-8 round-trip, exactly one trailing
    # newline (no blank lines), and exactly one line of content.
    with open(path, "rb") as f:
        raw = f.read()
    expected = (ENTRY + "\n").encode("utf-8")
    if raw != expected:
        raise SystemExit("verification failed: entry.txt does not match the pitch")
    if len(raw) != len(expected):
        raise SystemExit("verification failed: entry.txt byte length mismatch")
    text = raw.decode("utf-8")
    if text.count("\n") != 1 or not text.endswith("\n"):
        raise SystemExit(
            "verification failed: entry.txt must be exactly one line "
            "with a single trailing newline"
        )
    if text.rstrip("\n") != ENTRY:
        raise SystemExit("verification failed: entry.txt content drifted")
    print(f"wrote {path} ({len(ENTRY)} chars)")
    print(ENTRY)


if __name__ == "__main__":
    main()
