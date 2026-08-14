"""The sync tool must name the files it actually wrote.

It used to print a decorative label — `python/ocn-1.csv` for a file that
lives at `src/ocn/data/ocn-1.csv`. On 2026-08-05 that line was pasted
into a `git add`, git refused the whole invocation because `python/` does
not exist, `2>/dev/null` swallowed the error, and commit 7a598dc shipped
a message describing 155 alias changes it did not contain. A path a
reader can act on is the fix.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SYNC = REPO_ROOT / "tools" / "sync_package_data.py"


class SyncPackageDataTests(unittest.TestCase):
    def test_reported_paths_are_the_files_on_disk(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            py_dir = Path(tmp) / "py"
            rs_dir = Path(tmp) / "rs"
            result = subprocess.run(
                [sys.executable, str(SYNC), "--apply",
                 "--data-dir", str(py_dir), "--rust-data-dir", str(rs_dir)],
                capture_output=True, text=True, cwd=REPO_ROOT,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            wrote = [line.split(None, 1)[1]
                     for line in result.stdout.splitlines()
                     if line.startswith("WROTE ")]
            self.assertTrue(wrote, f"expected WROTE lines, got {result.stdout!r}")
            for reported in wrote:
                path = Path(reported)
                if not path.is_absolute():
                    path = REPO_ROOT / path
                self.assertTrue(
                    path.is_file(),
                    f"reported {reported!r}, which is not a file "
                    f"(resolved to {path})",
                )


if __name__ == "__main__":
    unittest.main()
