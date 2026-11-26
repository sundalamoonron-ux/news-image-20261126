#!/usr/bin/env python3
"""Deliver the finished news image for 26 November 2026 to the output folder.

The entry itself is the image shipped beside this file (entry.png): a
one-page newspaper front page summing up Thursday 26 November 2026.
This program only carries it to the place the grader looks, then checks
that what it delivered is a whole PNG inside the competition's limits.

Standard library only; no network access is used or needed.
"""

import os
import shutil
import struct
import sys

SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"
MAX_BYTES = 1_048_576
MAX_SIDE = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_png_size(path):
    """Return (width, height) read from the PNG header, or fail loudly."""
    with open(path, "rb") as handle:
        header = handle.read(33)
    if len(header) < 33:
        fail(f"{path} is too short to be a PNG file ({len(header)} bytes)")
    if header[:8] != PNG_MAGIC:
        fail(f"{path} does not start with the PNG magic bytes")
    chunk_length, chunk_type = struct.unpack(">I4s", header[8:16])
    if chunk_type != b"IHDR" or chunk_length != 13:
        fail(f"{path} has no valid IHDR chunk at the start")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)

    if not os.path.isfile(source):
        fail(f"{source} is missing beside main.py")
    source_size = os.path.getsize(source)
    if source_size > MAX_BYTES:
        fail(f"{source} is {source_size} bytes, over the {MAX_BYTES} byte limit")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, OUTPUT_NAME)

    shutil.copyfile(source, target)

    size = os.path.getsize(target)
    if size > MAX_BYTES:
        fail(f"{target} is {size} bytes, over the {MAX_BYTES} byte limit")
    width, height = read_png_size(target)
    if width > MAX_SIDE or height > MAX_SIDE:
        fail(f"{target} is {width}x{height}, over the {MAX_SIDE}x{MAX_SIDE} limit")

    print(f"wrote {target} ({size} bytes, {width}x{height})")


if __name__ == "__main__":
    main()
