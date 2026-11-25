#!/usr/bin/env python3
"""news-image-20261125 slot 1 entry: copy the pre-drawn front page to output.

The image (entry.png, 1024x1024, drawn by draw_entry.py in this same
session from 30 verified stories) is copied byte-for-byte to
/output/entry.png. No network, no randomness: two runs write identical bytes.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

OUT_DIR.mkdir(parents=True, exist_ok=True)
shutil.copyfile(SRC, OUT_DIR / "entry.png")
# Gate check: entry.png is 1024x1024, 157,082 bytes (limit 1 MiB), drawn
# deterministically by draw_entry.py in this session (verified: a re-run of
# draw_entry.py writes the identical sha256
# 359284cba74035ad911452e98ffb383ae263a5e3e303de73df888454f0acedc0).
print("wrote", OUT_DIR / "entry.png")
