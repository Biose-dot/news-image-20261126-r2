#!/usr/bin/env python3
"""Entrypoint for the news-image-20261126 entry (Python 3.13, stdlib only).

Copies the front-page artwork (entry.png, drawn in code by
draw_frontpage.py and committed beside this file) to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).

The program performs no network access, reads no clock and uses no
randomness: every run writes the same bytes. It verifies the artwork
before and after the copy (PNG signature, 1024x1024 IHDR dimensions,
trailing IEND chunk, size and SHA-256) through a staging file, so a
broken file is never delivered; any failed check exits non-zero.
"""
import hashlib
import os
import shutil
import struct
import sys

EXPECTED_SHA256 = "43f527d422342a090329ced85515ef368a6111f9770ccacb9022fe1a3082356c"
EXPECTED_SIZE = 167509
WIDTH, HEIGHT = 1024, 1024


def fail(message):
    print(f"main.py: error: {message}", file=sys.stderr)
    sys.exit(1)


def check_png(path):
    """Validate the artwork file and return its bytes."""
    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError as exc:
        fail(f"cannot read {path}: {exc}")
    if len(data) != EXPECTED_SIZE:
        fail(f"{path}: size {len(data)} != expected {EXPECTED_SIZE}")
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        fail(f"{path}: SHA-256 mismatch")
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        fail(f"{path}: bad PNG signature")
    if len(data) < 33 or data[12:16] != b"IHDR":
        fail(f"{path}: missing IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (WIDTH, HEIGHT):
        fail(f"{path}: dimensions {width}x{height} != {WIDTH}x{HEIGHT}")
    if data[-12:] != b"\x00\x00\x00\x00IEND\xaeB`\x82":
        fail(f"{path}: missing trailing IEND chunk")
    return data


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    data = check_png(source)
    target = os.path.join(out_dir, "entry.png")
    staging = target + ".staging"
    try:
        with open(staging, "wb") as fh:
            fh.write(data)
        check_png(staging)
        shutil.move(staging, target)
    finally:
        # Never leave a half-written staging file behind on failure.
        if os.path.exists(staging):
            os.unlink(staging)
    with open(target, "rb") as fh:
        delivered = fh.read()
    if delivered != data:
        fail("delivered file differs from verified artwork")
    print(f"main.py: wrote {target} "
          f"({len(delivered)} bytes, sha256 "
          f"{hashlib.sha256(delivered).hexdigest()[:16]}...)")


if __name__ == "__main__":
    main()
