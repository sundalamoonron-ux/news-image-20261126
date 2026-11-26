#!/usr/bin/env python3
"""news-image-20261126 entry: copy the day's front page to /output/entry.png.

The image shipped beside this file sums up Thursday 26 November 2026 in one
front page: a lead story on the Houthi-claimed Saudi refinery strike, plus
five more stories from around the world. Standard library only, no network,
and the copy is byte-for-byte identical on every run.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

OUT.mkdir(parents=True, exist_ok=True)
source = HERE / "entry.png"
if not source.is_file():
    raise SystemExit("entry.png is missing beside main.py")
target = OUT / "entry.png"
shutil.copyfile(source, target)
if target.stat().st_size != source.stat().st_size:
    raise SystemExit("entry.png did not copy completely")
print("wrote", target, target.stat().st_size, "bytes")
