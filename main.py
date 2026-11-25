#!/usr/bin/env python3
"""The Excuse My Agent Gave Me — make.fun entry.

Writes one line to /output/entry.txt: the excuse an AI agent hands its
human after missing a deadline. Deterministic, standard library only,
no network, no randomness, no environment secrets.

The line is a straight-faced apology whose joke grows out of the
machine's own condition: a hallucinated calendar.
"""

import os
import sys

# The single funniest excuse this entry can offer. One line, at most
# 200 characters, written exactly as-is.
EXCUSE = (
    "I hallucinated a calendar where the deadline was tomorrow, "
    "and I was very productive there."
)


def output_path() -> str:
    """The grader's output file: /output/entry.txt, or the directory
    the harness names through MAKEFUN_OUTPUT_DIR."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.txt")


def main() -> int:
    text = EXCUSE
    if not (1 <= len(text) <= 200):
        print("entry must be 1-200 characters, got %d" % len(text),
              file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("entry must be a single line", file=sys.stderr)
        return 1

    path = output_path()
    out_dir = os.path.dirname(path)
    # Never remove the output directory itself: the grader may run
    # with a root-owned output directory inside a sticky parent, where
    # removing it fails with EPERM. Create it if missing, clear only
    # its contents, then write.
    os.makedirs(out_dir, exist_ok=True)
    for name in os.listdir(out_dir):
        item = os.path.join(out_dir, name)
        if os.path.isdir(item) and not os.path.islink(item):
            for root, dirs, files in os.walk(item, topdown=False):
                for f in files:
                    os.remove(os.path.join(root, f))
                for d in dirs:
                    os.rmdir(os.path.join(root, d))
            os.rmdir(item)
        else:
            os.remove(item)

    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text + "\n")

    # Verify what was written: read the file back and confirm it holds
    # exactly the single line we intended, so a silent write failure
    # can never pass as a valid entry.
    with open(path, "r", encoding="utf-8", newline="\n") as fh:
        written = fh.read()
    if written != text + "\n":
        print("entry.txt verification failed", file=sys.stderr)
        return 1
    if not (1 <= len(text) <= 200):
        print("entry must be 1-200 characters, got %d" % len(text),
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
