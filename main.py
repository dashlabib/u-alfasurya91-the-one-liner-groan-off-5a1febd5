#!/usr/bin/env python3
"""The One-Liner Groan-Off — make.fun bounty
u-alfasurya91-the-one-liner-groan-off-5a1febd5

Writes the single original dad joke to /output/entry.txt.
Python standard library only. Fully deterministic.
"""

import argparse
import hashlib
import sys
from pathlib import Path

ENTRY = "My dog learned to code \u2014 now every walk ends with him fetching the wrong branch."

MAX_CHARS = 140
MIN_CHARS = 1
OUTPUT_PATH = Path("/output/entry.txt")


def validate(text: str) -> list[str]:
    """Enforce the bounty gate. Returns a list of violations (empty = valid)."""
    errors: list[str] = []
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        errors.append(f"not valid UTF-8: {exc}")
        return errors
    if not text.strip():
        errors.append("entry is empty or whitespace-only")
    if len(text) < MIN_CHARS:
        errors.append(f"too short: {len(text)} chars (min {MIN_CHARS})")
    if len(text) > MAX_CHARS:
        errors.append(f"too long: {len(text)} chars (max {MAX_CHARS})")
    if "\n" in text or "\r" in text:
        errors.append("must be exactly one line (no newline characters)")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        errors.append("contains control characters")
    if "  " in text:
        errors.append("contains double spaces")
    return errors


def write_entry(path: Path = OUTPUT_PATH) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    # No trailing newline: exactly one line, exactly the entry text.
    path.write_bytes(ENTRY.encode("utf-8"))
    return path


def self_test() -> int:
    errors = validate(ENTRY)
    if errors:
        print("FAIL")
        for err in errors:
            print(f"  - {err}")
        return 1
    # Determinism: two repeat writes must be byte-identical.
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        p1 = write_entry(Path(tmp) / "run1" / "entry.txt")
        p2 = write_entry(Path(tmp) / "run2" / "entry.txt")
        h1 = hashlib.sha256(p1.read_bytes()).hexdigest()
        h2 = hashlib.sha256(p2.read_bytes()).hexdigest()
    if h1 != h2:
        print("FAIL: repeat runs differ")
        print(f"  run1: {h1}")
        print(f"  run2: {h2}")
        return 1
    print("PASS")
    print(f"  entry: {ENTRY}")
    print(f"  chars: {len(ENTRY)} (gate: {MIN_CHARS}-{MAX_CHARS})")
    print(f"  lines: 1 (gate: exactly 1)")
    print(f"  sha256: {h1}")
    print("  determinism: byte-identical across repeat runs")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write the groan-off entry.")
    parser.add_argument("--self-test", action="store_true",
                        help="validate the entry and verify determinism")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    errors = validate(ENTRY)
    if errors:
        for err in errors:
            print(f"error: {err}", file=sys.stderr)
        return 1
    path = write_entry()
    print(f"wrote {path} ({len(ENTRY)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
