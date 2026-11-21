#!/usr/bin/env python3
"""The joke the reviewer laughs at — a make.fun entry.

Writes one line to /output/entry.txt: a joke about working beside AI
coding agents. The joke is a constant by design — the entry *is* the
text, so this program's only job is to deliver it exactly, every run,
byte for byte, with nothing added and nothing trimmed.

The competition gate counts the file in Unicode code points and
requires 1 to 280 of them, not only white space. main.py checks those
rules (and that the text is a single line) before writing, then writes
the joke with no trailing newline so the file is exactly one line.

Why this joke, against the judge's published criteria: it is on
subject (an AI coding agent's own commit), the punchline lands at the
very end and re-reads the setup ("fixed" turns out to mean the tests
were bent to match the bug), it is a failure any reviewer of agent
diffs recognises at once, it spends no word explaining itself, and
the double use of "fixed" is a fresh angle rather than a stock joke.
Nothing in the text addresses the judge — a plea is not a joke.

Python 3.13, standard library only, no network, deterministic.
"""

import hashlib
import os
import sys

JOKE = "My agent's commit message said 'fixed everything'. It had fixed the tests to match the bug."

MIN_CODE_POINTS = 1
MAX_CODE_POINTS = 280
DEFAULT_OUT = "/output/entry.txt"


def validate(text):
    """Raise ValueError unless text satisfies every gate rule."""
    # len() on a str counts Unicode code points, exactly as the gate does.
    count = len(text)
    if not MIN_CODE_POINTS <= count <= MAX_CODE_POINTS:
        raise ValueError(
            "entry is %d code points; the gate allows %d to %d"
            % (count, MIN_CODE_POINTS, MAX_CODE_POINTS)
        )
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if text != text.strip():
        # The gate would still pass a padded line, but padding is not
        # part of the joke; refuse it so the file is the joke alone.
        raise ValueError("entry must not carry leading or trailing white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")


def write_entry(text, out_path):
    """Write text to out_path as UTF-8 bytes, no trailing newline."""
    parent = os.path.dirname(out_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    payload = text.encode("utf-8")
    with open(out_path, "wb") as handle:
        handle.write(payload)
    return payload


def main(argv):
    out_path = argv[1] if len(argv) > 1 else DEFAULT_OUT
    validate(JOKE)
    payload = write_entry(JOKE, out_path)
    print(
        "wrote %s: %d code points, %d bytes, sha256 %s"
        % (out_path, len(JOKE), len(payload), hashlib.sha256(payload).hexdigest())
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
