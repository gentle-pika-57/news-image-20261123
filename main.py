#!/usr/bin/env python3
"""Render poster.html to /output/entry.png with headless Chromium.

Standard library only. No network access. The render is meant to be
deterministic: fixed 1024x1024 viewport, device scale factor 1, hidden
scrollbars, animations frozen by a virtual time budget, and no background
network activity while the shot is taken.
"""

import os
import shutil
import struct
import subprocess
import sys
from pathlib import Path

WIDTH = 1024
HEIGHT = 1024
MAX_BYTES = 1048576
VIRTUAL_TIME_BUDGET_MS = 8000

SYSTEM_BINARIES = (
    "chromium",
    "chromium-browser",
    "google-chrome",
    "google-chrome-stable",
)

# Layouts seen under Playwright's cache, newest first by directory name.
PLAYWRIGHT_SUBPATHS = (
    "chrome-linux64/chrome",
    "chrome-linux/chrome",
    "chrome-headless-shell-linux64/chrome-headless-shell",
    "chrome-linux/headless_shell",
)


def _playwright_roots():
    roots = []
    home = Path.home()
    roots.append(home / ".cache" / "ms-playwright")
    roots.append(Path("/root/.cache/ms-playwright"))
    roots.append(Path("/ms-playwright"))
    return roots


def find_chromium():
    """Return a Chromium executable path, preferring a full Chromium build."""
    for name in SYSTEM_BINARIES:
        path = shutil.which(name)
        if path and os.access(path, os.X_OK):
            return path
    full = []
    shell = []
    for root in _playwright_roots():
        if not root.is_dir():
            continue
        for entry in sorted(root.iterdir(), reverse=True):
            if not entry.name.startswith("chromium"):
                continue
            for sub in PLAYWRIGHT_SUBPATHS:
                candidate = entry / sub
                if candidate.is_file() and os.access(candidate, os.X_OK):
                    if "headless" in sub:
                        shell.append(str(candidate))
                    else:
                        full.append(str(candidate))
    for path in full + shell:
        return path
    return None


def check_png(path):
    """Confirm the screenshot is a 1024x1024 PNG within the size limit."""
    with open(path, "rb") as handle:
        head = handle.read(33)
    if len(head) < 33 or head[:8] != b"\x89PNG\r\n\x1a\n":
        print("output is not a PNG file", file=sys.stderr)
        return False
    if head[12:16] != b"IHDR":
        print("PNG has no IHDR chunk", file=sys.stderr)
        return False
    width, height = struct.unpack(">II", head[16:24])
    if (width, height) != (WIDTH, HEIGHT):
        print("PNG is %dx%d, expected 1024x1024" % (width, height),
              file=sys.stderr)
        return False
    return True


def main():
    here = Path(__file__).resolve().parent
    poster = here / "poster.html"
    if not poster.is_file():
        print("poster.html not found next to main.py", file=sys.stderr)
        return 1

    out_dir = Path("/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "entry.png"

    chrome = find_chromium()
    if chrome is None:
        print("no Chromium binary found", file=sys.stderr)
        return 1

    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--hide-scrollbars",
        "--force-device-scale-factor=1",
        "--window-size=%d,%d" % (WIDTH, HEIGHT),
        "--disable-background-networking",
        "--disable-component-update",
        "--disable-sync",
        "--disable-lcd-text",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=%d" % VIRTUAL_TIME_BUDGET_MS,
        "--screenshot=%s" % out_path,
        poster.as_uri(),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=55)
    if result.returncode != 0:
        sys.stderr.write(result.stdout)
        sys.stderr.write(result.stderr)
        return 1
    if not out_path.is_file():
        print("screenshot was not written", file=sys.stderr)
        return 1

    size = out_path.stat().st_size
    print("wrote %s (%d bytes)" % (out_path, size))
    if size > MAX_BYTES:
        print("entry.png exceeds 1 MiB", file=sys.stderr)
        return 1
    if not check_png(out_path):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
