#!/usr/bin/env python3
"""Copy the pre-rendered entry.png to the output directory.

The competition image is already rendered and stored in the repository as
entry.png. This program only validates that image and copies its exact
bytes to the grader's output directory. It needs no network, no browser
and no third-party libraries -- Python's standard library only.
"""

import os
import struct
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
MAX_FILE_SIZE = 1_048_576  # 1 MiB
SOURCE_NAME = "entry.png"


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    return 1


def validate_png(data):
    """Return an error string if data is not a valid 1024x1024 PNG."""
    if len(data) < 8 or data[:8] != PNG_SIGNATURE:
        return "not a PNG file (bad signature)"
    if len(data) < 33:
        return "PNG file is too short to contain an IHDR chunk"
    # The IHDR chunk starts right after the 8-byte signature:
    # 4 bytes chunk length, 4 bytes chunk type "IHDR",
    # then 4 bytes width and 4 bytes height (big-endian).
    length = struct.unpack(">I", data[8:12])[0]
    chunk_type = data[12:16]
    if chunk_type != b"IHDR" or length != 13:
        return "first chunk is not a valid IHDR chunk"
    width, height = struct.unpack(">II", data[16:24])
    if width != EXPECTED_WIDTH or height != EXPECTED_HEIGHT:
        return f"image is {width}x{height}, expected {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}"
    return None


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)

    try:
        with open(source, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        return fail(f"cannot read {source}: {exc}")

    if len(data) > MAX_FILE_SIZE:
        return fail(
            f"entry.png is {len(data)} bytes, over the {MAX_FILE_SIZE} byte limit"
        )

    problem = validate_png(data)
    if problem is not None:
        return fail(problem)

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    destination = os.path.join(output_dir, SOURCE_NAME)

    try:
        os.makedirs(output_dir, exist_ok=True)
        with open(destination, "wb") as handle:
            handle.write(data)
        written = os.path.getsize(destination)
    except OSError as exc:
        return fail(f"cannot write {destination}: {exc}")
    if written != len(data):
        return fail(f"wrote {written} bytes, expected {len(data)}")

    print(f"copied {len(data)} bytes to {destination}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
