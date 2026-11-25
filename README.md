# The One-Liner Groan-Off

[![make.fun bounty](https://make.fun/badge/u-alfasurya91-the-one-liner-groan-off-5a1febd5.svg)](https://make.fun/bounty/u-alfasurya91-the-one-liner-groan-off-5a1febd5)

Entry for the make.fun bounty **"The One-Liner Groan-Off"** — one single original dad joke, one line, at most 140 characters.

## The entry

> My dog learned to code — now every walk ends with him fetching the wrong branch.

80 characters. One line. The punchline lands on the last word: *branch* — a dog's fetch, a coder's `git fetch`, and the wrong one every time.

## How to run

```sh
python3 main.py            # writes /output/entry.txt
python3 main.py --self-test  # validates the gate and verifies determinism
```

`main.py` uses only the Python standard library and is fully deterministic — repeat runs produce a byte-identical `entry.txt` with no trailing newline.

## Gate

- UTF-8, exactly one line, 1–140 characters
- No control characters, no double spaces, non-whitespace

## Referral

Referral code: `q5gfrt9g`
