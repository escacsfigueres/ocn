"""A coverage check that cannot read the fonts has not checked anything.

`python3 tools/subset_fonts.py` printed "unreadable" for all six woff2
faces — brotli was not installed — and then concluded "every face covers
the catalogue" and exited 0. That is the answer the roadmap was waiting
on, delivered by a check that verified nothing.

These tests need neither fonttools nor brotli: a face that cannot be
opened is exactly the case under test, and an absent library opens no
files either.
"""
from __future__ import annotations

import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

import subset_fonts  # noqa: E402


class ReportTests(unittest.TestCase):
    def test_a_face_it_cannot_open_is_counted_as_unreadable(self) -> None:
        with TemporaryDirectory() as tmp:
            (Path(tmp) / "spectral-400.woff2").write_bytes(b"not a font")
            out = io.StringIO()
            with mock.patch.object(subset_fonts, "FONTS", Path(tmp)):
                with redirect_stdout(out):
                    missing, unreadable = subset_fonts.report()
        self.assertEqual(unreadable, 1)
        self.assertEqual(missing, 0, "nothing was read, so nothing has gaps")
        self.assertIn("unreadable", out.getvalue())

    def test_an_unreadable_face_is_never_reported_as_a_pass(self) -> None:
        """The defect itself: `missing == 0` used to mean success even when
        it meant "opened nothing"."""
        out = io.StringIO()
        with mock.patch.object(subset_fonts, "report", lambda: (0, 6)):
            with mock.patch.dict(sys.modules, {"fontTools": mock.Mock()}):
                with redirect_stdout(out):
                    code = subset_fonts.main([])
        self.assertNotEqual(code, 0)
        self.assertNotIn("every face covers the catalogue", out.getvalue())
        self.assertIn("cannot answer", out.getvalue())

    def test_the_shipped_fonts_cover_the_catalogue(self) -> None:
        """Skipped where a woff2 cannot be opened, because that is a
        missing dependency and not a defect in the fonts — but never
        silently passed, which is what the tool used to do."""
        try:
            import brotli  # noqa: F401
            import fontTools  # noqa: F401
        except ImportError:
            self.skipTest("woff2 faces cannot be read here "
                          "(pip install fonttools brotli)")
        out = io.StringIO()
        with mock.patch.object(subset_fonts, "FONTS", REPO_ROOT / "web" / "fonts"):
            with redirect_stdout(out):
                code = subset_fonts.main([])
        self.assertEqual(code, 0, out.getvalue())


if __name__ == "__main__":
    unittest.main()
