"""Regression tests for the manual PyPI publishing workflow."""

from pathlib import Path

WORKFLOW = Path(".github/workflows/publish-pypi.yml")


def _workflow_text() -> str:
    """Return the PyPI publishing workflow text."""
    return WORKFLOW.read_text(encoding="utf-8")


def _validate_release_tag_step() -> str:
    """Return the shell body for the release-tag validation step."""
    workflow = _workflow_text()
    marker = "      - name: Validate release tag\n"
    start = workflow.index(marker)
    end = workflow.index("      - name: Checkout tag\n", start)
    return workflow[start:end]


def test_publish_workflow_validates_tag_before_checkout() -> None:
    """Reject unsafe tag inputs before checking out attacker-controlled refs."""
    workflow = _workflow_text()

    assert workflow.index("      - name: Validate release tag\n") < workflow.index(
        "      - name: Checkout tag\n",
    )


def test_publish_workflow_passes_tag_input_through_environment() -> None:
    """Avoid direct shell interpolation of workflow_dispatch input."""
    step = _validate_release_tag_step()

    assert "TAG: ${{ inputs.tag }}" in step
    assert 'case "${{ inputs.tag }}"' not in step
    assert "refs/tags/${{ inputs.tag }}" not in step


def test_publish_workflow_rejects_non_semver_tag_names() -> None:
    """Keep tag validation strict enough to reject shell metacharacter payloads."""
    step = _validate_release_tag_step()

    assert '[[ ! "$TAG" =~ ^v[0-9]+[.][0-9]+[.][0-9]+$ ]]' in step
