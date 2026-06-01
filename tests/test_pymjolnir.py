"""Smoke tests until the public API grows."""

from pathlib import Path

import pymjolnir

REPO_ROOT = Path(__file__).resolve().parents[1]
PYPI_PUBLISH_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "publish-pypi.yml"


def test_package_importable() -> None:
    """Import package; module docstring should be present."""
    assert pymjolnir.__doc__


def test_pypi_publish_validates_tag_input_before_checkout() -> None:
    """Reject malicious manual tags before using them in checkout."""
    workflow = PYPI_PUBLISH_WORKFLOW.read_text()

    validation_step = "      - name: Validate release tag input\n"
    checkout_step = "      - name: Checkout tag\n"

    assert workflow.index(validation_step) < workflow.index(checkout_step)


def test_pypi_publish_shell_uses_validated_env_tag() -> None:
    """Avoid direct GitHub expression interpolation inside shell scripts."""
    workflow = PYPI_PUBLISH_WORKFLOW.read_text()

    validation_start = workflow.index("      - name: Validate release tag input\n")
    checkout_start = workflow.index("      - name: Checkout tag\n")
    validation_step = workflow[validation_start:checkout_start]
    verify_step = workflow[workflow.index("      - name: Verify checked-out release tag\n") :]

    assert "RELEASE_TAG: ${{ inputs.tag }}" in validation_step
    assert "${{ inputs.tag }}" not in validation_step.split("run: |", maxsplit=1)[1]
    assert 'git rev-parse --verify --end-of-options "refs/tags/$RELEASE_TAG"' in verify_step
