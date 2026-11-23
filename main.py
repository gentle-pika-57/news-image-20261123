"""Emit the 23 November 2026 front page as a PNG file.

The artwork lives next to this script as ``entry.png`` — a 1024x1024
newspaper front page summing up Monday 23 November 2026 in 44 verified
stories (11 illustrated leads, a dotted world map, an "also on" list,
stat boxes and a date-check strip).  Running the script copies those
exact bytes to ``entry.png`` inside the output directory
(``MAKEFUN_OUTPUT_DIR`` when set, ``/output`` otherwise), creating the
directory first when it does not exist.
"""

import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def output_dir() -> Path:
    """Where the finished front page goes."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main() -> None:
    if not SOURCE.is_file():
        sys.exit(f"missing artwork: {SOURCE}")
    target = output_dir()
    target.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, target / "entry.png")


if __name__ == "__main__":
    main()
