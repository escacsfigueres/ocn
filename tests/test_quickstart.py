"""The README quickstart is executable, and its printed answers are true.

Roadmap H2.2: a stranger copies the block at the top of the README into
a shell and it works, forever. The only way to keep that promise is to
run the block itself rather than a paraphrase of it, so this test
*extracts* the fenced Python from `README.md` and executes it line by
line, comparing every `# -> value` comment against what the line really
evaluates to.

The convention the README follows, and this file enforces:

    expression            # -> repr of the expected value

Lines without a `# ->` comment are executed for their effect (imports,
assignments). A statement that spans more than one line is not
supported on purpose — a quickstart that needs one is too long.

Run from a checkout without installing anything:

    python3 -m unittest discover -s tests
"""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from ocn.cli import build_parser  # noqa: E402

README = REPO_ROOT / "README.md"
SECTION = "## Five-minute quickstart"
EXPECT = "# ->"
FENCE_RE = re.compile(r"^```(\w*)\s*$")
# Minimum evidence that the gate is still a gate: someone who guts the
# expectations to make a failure go away trips this instead.
MIN_EXPECTATIONS = 4


def read_section() -> list[str]:
    """The lines of the README's quickstart section."""
    lines = README.read_text(encoding="utf-8").splitlines()
    start = lines.index(SECTION)
    for end in range(start + 1, len(lines)):
        if lines[end].startswith("## "):
            return lines[start:end]
    return lines[start:]


def fenced_blocks(lines: list[str], language: str) -> list[list[str]]:
    """Every fenced code block of one language, in order."""
    blocks: list[list[str]] = []
    current: list[str] | None = None
    for line in lines:
        fence = FENCE_RE.match(line)
        if fence and current is None:
            current = [] if fence.group(1) == language else None
            if current is None:
                continue
            blocks.append(current)
            continue
        if fence and current is not None:
            current = None
            continue
        if current is not None:
            current.append(line)
    return blocks


def split_expectation(line: str) -> tuple[str, str] | None:
    """Split ``expr  # -> expected`` into its two halves."""
    if EXPECT not in line:
        return None
    code, _, expected = line.partition(EXPECT)
    return code.rstrip(), expected.strip()


class QuickstartTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.section = read_section()
        blocks = fenced_blocks(cls.section, "python")
        assert blocks, f"no ```python block under {SECTION!r} in README.md"
        cls.block = blocks[0]

    def test_the_block_runs_and_every_expectation_holds(self) -> None:
        # exec/eval are the point of a doctest gate: the code under test is
        # the README of this repository, version-controlled alongside it and
        # no more privileged than the test file itself. Nothing here reads
        # untrusted input.
        namespace: dict[str, object] = {}
        checked = 0
        for number, line in enumerate(self.block, start=1):
            if not line.strip():
                continue
            self.assertFalse(
                line.startswith((" ", "\t")),
                f"README quickstart line {number} is indented; the runner "
                "executes one statement per line",
            )
            expectation = split_expectation(line)
            if expectation is None:
                exec(compile(line, "README.md", "exec"), namespace)  # noqa: S102
                continue
            code, expected = expectation
            with self.subTest(line=number, code=code):
                value = eval(compile(code, "README.md", "eval"), namespace)  # noqa: S307
                self.assertEqual(
                    repr(value),
                    expected,
                    f"README quickstart line {number} claims {expected}",
                )
            checked += 1
        self.assertGreaterEqual(checked, MIN_EXPECTATIONS)

    def test_the_block_shows_the_four_entry_points(self) -> None:
        """Load, name, breadcrumb, ECO, position: the tour, not a teaser."""
        body = "\n".join(self.block)
        for call in ("Catalog.load(", "by_slug(", "parents(", "by_eco(", "by_fen("):
            self.assertIn(call, body)

    def test_the_block_is_short_enough_to_read(self) -> None:
        code = [line for line in self.block if line.strip()]
        self.assertLessEqual(len(code), 8, "a five-minute quickstart fits on a screen")

    def test_the_shell_commands_are_real_subcommands(self) -> None:
        """`ocn annotate ...` in the README must be a command that exists."""
        known = set()
        for action in build_parser()._subparsers._group_actions:  # noqa: SLF001
            known.update(action.choices)
        commands = [
            line.split()[1]
            for block in fenced_blocks(self.section, "bash")
            for line in block
            if line.startswith("ocn ")
        ]
        self.assertIn("annotate", commands)
        for command in commands:
            self.assertIn(command, known)

    def test_the_install_line_is_honest(self) -> None:
        """The package is live on PyPI (1.2.1, 2026-07-30), so the
        quickstart claims the real install and nothing more."""
        bash = "\n".join(line for block in fenced_blocks(self.section, "bash") for line in block)
        self.assertIn("pip install ocn-chess", bash)
        self.assertNotIn("next tagged release", bash)


if __name__ == "__main__":
    unittest.main()
