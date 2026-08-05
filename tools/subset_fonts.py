#!/usr/bin/env python3
"""Rebuild web/fonts from upstream, with the coverage this catalogue needs.

The faces shipped here were the Google Fonts *latin* subset, which stops at
Latin-1. The catalogue does not: Oldřich Duras needs ř, and there are ć, č and
ė elsewhere. A missing glyph does not fail loudly — the browser silently
substitutes a face from whatever machine is rendering, so the monograph was
embedding Georgia and Helvetica into a PDF whose colophon claims to be
reproducible.

The range below is stated rather than derived from today's data. Subsetting to
exactly the characters currently in the catalogue would put the same trap back
in place for the next Czech or Lithuanian name. Latin Extended-A covers every
European language a chess name is likely to arrive in, and costs under a
kilobyte per face.

    pip install fonttools brotli
    python3 tools/subset_fonts.py            # check what is installed
    python3 tools/subset_fonts.py --write    # fetch, subset and replace

u_DIN 1451 Mittelschrift is not touched. It is a road-sign face with 266
glyphs, it is not on Google Fonts, and the monograph handles its gaps by
falling back to Spectral rather than to the system.
"""

import argparse
import sys
import tempfile
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FONTS = REPO / "web" / "fonts"

# basic Latin, Latin-1, Latin Extended-A, and the punctuation the volume sets
RANGES = ("U+0020-007E,U+00A0-00FF,U+0100-017F,U+2010-2027,U+2030,"
          "U+2039-203A,U+2044,U+2212,U+20AC")

FAMILIES = {
    "Spectral:ital,wght@0,400;0,600;1,400": {
        "Spectral Regular": "spectral-400",
        "Spectral SemiBold": "spectral-600",
        "Spectral Italic": "spectral-400i",
    },
    "IBM+Plex+Mono:wght@400;500;600": {
        "IBM Plex Mono Regular": "plexmono-400",
        "IBM Plex Mono Medium": "plexmono-500",
        "IBM Plex Mono SemiBold": "plexmono-600",
    },
}

CHECK = {"ć": 0x0107, "č": 0x010D, "ė": 0x0117, "ř": 0x0159}


def coverage(path):
    from fontTools.ttLib import TTFont
    f = TTFont(path)
    cm = set()
    for t in f["cmap"].tables:
        cm |= set(t.cmap.keys())
    return f["name"].getDebugName(4), cm


def report():
    missing = 0
    for p in sorted(FONTS.glob("*.woff2")) + sorted(FONTS.glob("*.ttf")):
        try:
            name, cm = coverage(p)
        except Exception as exc:                                  # noqa: BLE001
            print(f"  {p.name:<30} unreadable ({exc})")
            continue
        gaps = [c for c, cp in CHECK.items() if cp not in cm]
        # u_DIN is expected to be short; the monograph falls back to Spectral
        # for it, which is why Spectral has to be complete.
        expected = "uDIN" in p.name
        if gaps and not expected:
            missing += len(gaps)
        note = ("complete" if not gaps
                else f"missing {' '.join(gaps)}"
                     + (" (expected; falls back to Spectral)" if expected else ""))
        print(f"  {p.name:<30} {len(cm):>4} glyphs   {note}")
    return missing


def fetch_and_subset(tmp):
    from fontTools import subset
    written = []
    for family, wanted in FAMILIES.items():
        css = urllib.request.urlopen(
            f"https://fonts.googleapis.com/css2?family={family}&display=swap",
            timeout=60).read().decode()
        urls = [ln.split("url(")[1].split(")")[0]
                for ln in css.splitlines() if "url(" in ln]
        if not urls:
            raise SystemExit(f"error: no font files listed for {family}")
        for i, url in enumerate(urls):
            src = tmp / f"src-{family[:6]}-{i}.ttf"
            src.write_bytes(urllib.request.urlopen(url, timeout=120).read())
            full, _ = coverage(src)
            out_name = wanted.get(full)
            if not out_name:
                continue
            out = FONTS / f"{out_name}.woff2"
            subset.main([str(src), f"--unicodes={RANGES}", "--layout-features=*",
                         "--flavor=woff2", f"--output-file={out}",
                         "--no-hinting", "--desubroutinize"])
            written.append(out)
    return written


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--write", action="store_true",
                    help="fetch upstream and replace the files in web/fonts")
    args = ap.parse_args(argv)

    try:
        import fontTools  # noqa: F401
    except ImportError:
        print("error: fonttools is required", file=sys.stderr)
        return 2

    if not args.write:
        print("web/fonts as installed:")
        gaps = report()
        print(f"\n{'every face covers the catalogue' if not gaps else 'run with --write'}")
        return 0 if not gaps else 1

    try:
        import brotli  # noqa: F401
    except ImportError:
        print("error: brotli is required to write woff2", file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory() as d:
        written = fetch_and_subset(Path(d))
    print(f"rewrote {len(written)} faces from upstream:")
    return 0 if report() == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
