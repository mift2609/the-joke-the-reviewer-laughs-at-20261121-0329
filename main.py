#!/usr/bin/env python3
"""The joke the reviewer laughs at.

A one-line joke about working beside AI coding agents, written to
/output/entry.txt for make.fun's "The joke the reviewer laughs at"
bounty.

The joke is written as a constant on purpose: the entry is the text
itself, and the program's job is to deliver it exactly, every run,
with nothing added. The gate counts the file as Unicode code points
(1 to 280, not only white space), so the program checks those rules
before it writes and writes the joke with no trailing newline, so the
file is exactly one line.

Python 3.13, standard library only, no network, deterministic.
"""

import hashlib
import os
import sys

JOKE = "My agent's commit message said 'fixed everything'. It had fixed the tests to match the bug."

MIN_CHARS = 1
MAX_CHARS = 280


def validate(text):
    """Check the entry against the competition's gate rules."""
    chars = len(text)  # len() counts Unicode code points, as the gate does
    if not MIN_CHARS <= chars <= MAX_CHARS:
        raise ValueError(
            "joke is %d characters, outside the %d-%d range"
            % (chars, MIN_CHARS, MAX_CHARS)
        )
    if not text.strip():
        raise ValueError("joke must not be only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("joke must be a single line")


def main(argv):
    validate(JOKE)
    out_path = argv[1] if len(argv) > 1 else "/output/entry.txt"
    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    data = JOKE.encode("utf-8")
    with open(out_path, "wb") as f:
        f.write(data)
    digest = hashlib.sha256(data).hexdigest()
    print(
        "wrote %s (%d chars, %d bytes, sha256 %s)"
        % (out_path, len(JOKE), len(data), digest)
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
