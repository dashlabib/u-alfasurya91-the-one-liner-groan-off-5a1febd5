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
    if text != text.strip():
        errors.append("must not have leading or trailing whitespace")
    if text.rstrip() != text:
        errors.append("must not end with trailing whitespace")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        errors.append("contains control characters")
    if "  " in text:
        errors.append("contains double spaces")
    return errors


def write_entry(path: Path = OUTPUT_PATH) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    # No trailing newline: exactly one line, exactly the entry text.
    raw = ENTRY.encode("utf-8")
    path.write_bytes(raw)
    # Round-trip check: the written file must decode as UTF-8 and
    # re-encode to exactly the same bytes, with no newline anywhere
    # (including inside the entry constant itself).
    round_tripped = path.read_bytes()
    if round_tripped != raw:
        raise ValueError("written bytes do not match the entry encoding")
    decoded = round_tripped.decode("utf-8")  # raises on invalid UTF-8
    if decoded.encode("utf-8") != round_tripped:
        raise ValueError("written file does not round-trip UTF-8 exactly")
    if decoded != ENTRY or "\n" in decoded or "\r" in decoded:
        raise ValueError("written file content is not exactly the entry")
    return path


def self_test() -> int:
    errors = validate(ENTRY)
    if errors:
        print("FAIL")
        for err in errors:
            print(f"  - {err}")
        return 1
    # Determinism: three repeat writes must be byte-identical.
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        hashes = []
        for i in (1, 2, 3):
            p = write_entry(Path(tmp) / f"run{i}" / "entry.txt")
            hashes.append(hashlib.sha256(p.read_bytes()).hexdigest())
    h1 = hashes[0]
    if len(set(hashes)) != 1:
        print("FAIL: repeat runs differ")
        for i, h in enumerate(hashes, 1):
            print(f"  run{i}: {h}")
        return 1
    print("PASS")
    print(f"  entry: {ENTRY}")
    print(f"  chars: {len(ENTRY)} (gate: {MIN_CHARS}-{MAX_CHARS})")
    print(f"  lines: 1 (gate: exactly 1)")
    print(f"  sha256: {h1}")
    print("  determinism: byte-identical across 3 repeat runs")
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
