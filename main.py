#!/usr/bin/env python3
"""u-mang-the-moon-finally-answers-back-781a7ec1 entry.

Writes one original line, in the voice of the Moon answering at last,
to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output).
Python 3.13, stdlib only, fully deterministic:
the same line, byte-for-byte, every run.
"""

import os
import sys

ENTRY = (
    "Four billion years of wishes, howls, and 3 a.m. promises \u2014 "
    "and my answer is the same one I gave the dinosaurs: "
    "I heard you, and no, I\u2019m not doing anything about it."
)

# The gate accepts exactly one line of 1-240 characters, not only
# whitespace. Anything outside that shape would be rejected for shape
# rather than judged, so the entry refuses to ship it.
MIN_ENTRY_CHARS = 1
MAX_ENTRY_CHARS = 240


def validate_entry() -> None:
    """Check the line's shape before a single byte is written."""
    if not MIN_ENTRY_CHARS <= len(ENTRY) <= MAX_ENTRY_CHARS:
        raise SystemExit(
            f"entry is {len(ENTRY)} characters, "
            f"outside {MIN_ENTRY_CHARS}-{MAX_ENTRY_CHARS}"
        )
    if not ENTRY.strip():
        raise SystemExit("entry is only whitespace")
    if "\n" in ENTRY or "\r" in ENTRY:
        raise SystemExit("entry must be a single line")
    # The judge's first criterion is the Moon answering the wishes, the
    # howls and the late-night promises, and the fourth is the comeback
    # landing before the line ends: refuse to ship a line that lost
    # either before it ever reaches the judge.
    for word in ("wishes", "howls", "promises"):
        assert word in ENTRY, f"entry does not answer the {word}"
    assert ENTRY.endswith("about it."), "comeback does not land at the end"


def entry_path() -> str:
    """Resolve where the competition expects the single entry file."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, "entry.txt")


def verify_output(path: str, expected: str) -> None:
    """Re-read what was written and fail loudly if it is not the line."""
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != expected:
        raise SystemExit("entry.txt on disk does not match the entry")


def main() -> int:
    validate_entry()
    path = entry_path()
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY)
    verify_output(path, ENTRY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
