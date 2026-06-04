"""Tests for the PyPI release tag guard."""

from __future__ import annotations

import os
import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = REPO_ROOT / ".github" / "scripts" / "validate-release-tag.sh"
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "publish-pypi.yml"


class ReleaseTagValidationTests(unittest.TestCase):
    """Validate the manual PyPI workflow tag contract."""

    def run_validator(self, tag: str) -> subprocess.CompletedProcess[str]:
        """Run the release tag validator with a candidate tag."""
        env = os.environ.copy()
        env["RELEASE_TAG"] = tag
        return subprocess.run(
            ["bash", str(VALIDATOR)],
            check=False,
            env=env,
            capture_output=True,
            text=True,
        )

    def test_accepts_strict_release_tag(self) -> None:
        """A normal vX.Y.Z release tag is accepted."""
        result = self.run_validator("v1.2.3")

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_rejects_release_like_suffixes(self) -> None:
        """Suffixes must not pass as stable release tags."""
        for tag in ("v1.2.3-rc1", "v1.2.3.post1", "v1.2.3foo"):
            with self.subTest(tag=tag):
                result = self.run_validator(tag)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Tag must match the release pattern", result.stderr)

    def test_rejects_shell_metacharacters(self) -> None:
        """Shell metacharacters remain data and are rejected by the regex."""
        result = self.run_validator('v1.2.3"; echo pwned; #')

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Tag must match the release pattern", result.stderr)

    def test_workflow_validates_before_tag_checkout(self) -> None:
        """The user input is validated before the tag-specific checkout runs."""
        workflow = WORKFLOW.read_text(encoding="utf-8")

        self.assertLess(
            workflow.index("- name: Validate release tag input"),
            workflow.index("- name: Checkout tag"),
        )
        self.assertIn("RELEASE_TAG: ${{ inputs.tag }}", workflow)
        self.assertIn(
            'git rev-parse --verify --end-of-options "refs/tags/$RELEASE_TAG"',
            workflow,
        )


if __name__ == "__main__":
    unittest.main()
