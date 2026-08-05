#!/usr/bin/env python3
"""Write TrimBox and BleedBox into a PDF printed with bleed.

Chrome knows one page box. A printer needs three: the sheet it images
(MediaBox), the area that bleeds off the cut (BleedBox), and the cut itself
(TrimBox). Without them the file is a large page with no instruction, and the
press has to be told the trim by hand or guess it.

`tools/build_monograph.py --bleed` lays the trimmed page inside a sheet that is
larger by the bleed on every side, so the trim is simply the sheet inset by
that amount. This writes that down.

    python3 tools/set_pdf_boxes.py book.pdf --trim 210x297 --bleed 3

Leaves everything else alone: no re-compression, no colour conversion, no
downsampling. It only adds the boxes.
"""

import argparse
import sys
from pathlib import Path

MM = 72 / 25.4


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("pdf", type=Path)
    ap.add_argument("--trim", default="210x297",
                    help="trimmed page in millimetres, e.g. 210x297")
    ap.add_argument("--bleed", type=float, default=3.0,
                    help="bleed beyond the trim, in millimetres")
    ap.add_argument("--marks", type=float, default=5.0,
                    help="margin outside the bleed reserved for crop marks")
    ap.add_argument("--out", type=Path,
                    help="write here instead of in place")
    args = ap.parse_args(argv)

    try:
        import fitz
    except ImportError:
        print("error: PyMuPDF is required (pip install pymupdf)", file=sys.stderr)
        return 2

    try:
        tw, th = (float(x) for x in args.trim.lower().split("x"))
    except ValueError:
        print(f"error: --trim must look like 210x297, not {args.trim!r}", file=sys.stderr)
        return 2

    doc = fitz.open(args.pdf)
    off = (args.bleed + args.marks) * MM        # trim inset from the sheet edge
    b = args.bleed * MM
    expect_w = (tw + 2 * (args.bleed + args.marks)) * MM
    expect_h = (th + 2 * (args.bleed + args.marks)) * MM

    wrong = []
    for i, page in enumerate(doc, 1):
        r = page.mediabox
        if abs(r.width - expect_w) > 1.5 or abs(r.height - expect_h) > 1.5:
            wrong.append((i, round(r.width / MM, 1), round(r.height / MM, 1)))
    if wrong:
        print(f"error: {len(wrong)} page(s) are not {expect_w/MM:.0f}x{expect_h/MM:.0f}mm; "
              f"first is page {wrong[0][0]} at {wrong[0][1]}x{wrong[0][2]}mm.\n"
              "       Was this built with --bleed, and do --trim, --bleed and "
              "--marks match it?", file=sys.stderr)
        return 1

    for page in doc:
        r = page.mediabox
        trim = fitz.Rect(r.x0 + off, r.y0 + off, r.x1 - off, r.y1 - off)
        bleed = fitz.Rect(trim.x0 - b, trim.y0 - b, trim.x1 + b, trim.y1 + b)
        page.set_bleedbox(bleed)      # what may run off the cut
        page.set_trimbox(trim)        # the cut itself
        page.set_cropbox(r)           # a reader shows the sheet, marks and all

    out = args.out or args.pdf
    doc.save(str(out), incremental=out == args.pdf and args.out is None,
             encryption=fitz.PDF_ENCRYPT_KEEP)
    print(f"{doc.page_count} pages: MediaBox {expect_w/MM:.0f}x{expect_h/MM:.0f}mm, "
          f"BleedBox {tw + 2*args.bleed:.0f}x{th + 2*args.bleed:.0f}mm, "
          f"TrimBox {tw:.0f}x{th:.0f}mm -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
