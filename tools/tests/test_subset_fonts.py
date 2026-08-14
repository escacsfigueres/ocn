"""A coverage check that cannot read the fonts has not checked anything.

`python3 tools/subset_fonts.py` printed "unreadable" for all six woff2
faces — brotli was not installed — and then concluded "every face covers
the catalogue" and exited 0. That is the answer the roadmap was waiting
on, delivered by a check that verified nothing.
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
    def run_against(self, directory: Path) -> tuple[int, str]:
        out = io.StringIO()
        with mock.patch.object(subset_fonts, "FONTS", directory):
            with redirect_stdout(out):
                code = subset_fonts.main([])
        return code, out.getvalue()

    def test_an_unreadable_face_is_not_a_pass(self) -> None:
        with TemporaryDirectory() as tmp:
            (Path(tmp) / "spectral-400.woff2").write_bytes(b"not a font")
            code, output = self.run_against(Path(tmp))
        self.assertNotEqual(code, 0, output)
        self.assertNotIn("every face covers the catalogue", output)
        self.assertIn("unreadable", output)

    def test_the_shipped_fonts_cover_the_catalogue(self) -> None:
        """Skipped where a woff2 cannot be opened, because that is a
        missing dependency and not a defect in the fonts — but never
        silently passed, which is what the tool used to do."""
        try:
            import brotli  # noqa: F401
        except ImportError:
            self.skipTest("brotli not installed; woff2 faces cannot be read "
                          "(pip install fonttools brotli)")
        code, output = self.run_against(REPO_ROOT / "web" / "fonts")
        self.assertEqual(code, 0, output)


if __name__ == "__main__":
    unittest.main()
