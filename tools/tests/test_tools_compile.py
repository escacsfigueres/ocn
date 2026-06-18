"""Guard: every tool under tools/ must byte-compile.

The CI workflow byte-compiles the tools as a syntax smoke-test. That list used
to be hand-maintained and silently drifted out of date (build_lichess_xref.py,
generate_diacritic_manifest.py and ocn.py were all missing from it). CI now
globs tools/*.py; this test enforces the same invariant in the local suite, so
a tool with a syntax error — or a new tool — is caught before it reaches CI.
"""
from __future__ import annotations

import py_compile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOLS = REPO_ROOT / "tools"


class ToolsCompileTests(unittest.TestCase):
    def test_every_tool_byte_compiles(self) -> None:
        tools = sorted(TOOLS.glob("*.py"))
        self.assertTrue(tools, "expected to find tools under tools/")
        failures: list[str] = []
        for tool in tools:
            try:
                py_compile.compile(str(tool), doraise=True)
            except py_compile.PyCompileError as exc:  # pragma: no cover - failure path
                failures.append(f"{tool.name}: {exc.msg}")
        self.assertEqual(failures, [], f"tools failed to byte-compile: {failures}")


if __name__ == "__main__":
    unittest.main()
