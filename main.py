#!/usr/bin/env python3
"""Entry point for news-image-20261125.

Copies the committed front-page image (entry.png, drawn at build time by
draw.py) to /output/entry.png. Pure standard library, no network, no
drawing at runtime: the grader's python:3.13 sandbox has no fonts, so all
rendering happens at build time and this program only copies bytes.

Determinism: the copy is byte-for-byte, so two runs write identical files.
Verified locally with `env -i python3 main.py` against the committed image.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.environ.get("OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
