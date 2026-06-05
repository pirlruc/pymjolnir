"""Regression tests for GitHub Actions workflow safety invariants."""

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PUBLISH_PYPI_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "publish-pypi.yml"


def test_publish_pypi_tag_input_is_validated_before_checkout() -> None:
    """The manual publish workflow must reject unsafe tag input before checkout."""
    workflow = PUBLISH_PYPI_WORKFLOW.read_text(encoding="utf-8")

    validate_start = workflow.index("      - name: Validate release tag\n")
    checkout_start = workflow.index("      - name: Checkout tag\n")
    verify_start = workflow.index("      - name: Verify release tag\n")

    assert validate_start < checkout_start < verify_start

    validate_step = workflow[validate_start:checkout_start]
    verify_step = workflow[verify_start:]

    assert "TAG: ${{ inputs.tag }}" in validate_step
    assert "TAG: ${{ inputs.tag }}" in verify_step
    assert r"^v[0-9]+\.[0-9]+\.[0-9]+$" in validate_step
    assert "${{ inputs.tag }}" not in validate_step.replace("TAG: ${{ inputs.tag }}", "")
    assert "${{ inputs.tag }}" not in verify_step.replace("TAG: ${{ inputs.tag }}", "")
