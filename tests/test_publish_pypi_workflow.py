"""Regression tests for the manual PyPI publishing workflow."""

from pathlib import Path

WORKFLOW = Path(".github/workflows/publish-pypi.yml")


def _validate_release_tag_step() -> str:
    """Return the shell body for the release-tag validation step."""
    workflow = WORKFLOW.read_text(encoding="utf-8")
    marker = "      - name: Validate release tag\n"
    start = workflow.index(marker)
    end = workflow.index("      - name: Set up Python\n", start)
    return workflow[start:end]


def test_publish_workflow_passes_tag_input_through_environment() -> None:
    """Avoid direct shell interpolation of workflow_dispatch input."""
    step = _validate_release_tag_step()

    assert "TAG: ${{ inputs.tag }}" in step
    assert 'case "${{ inputs.tag }}"' not in step
    assert 'refs/tags/${{ inputs.tag }}' not in step


def test_publish_workflow_rejects_non_semver_tag_names() -> None:
    """Keep tag validation strict enough to reject shell metacharacter payloads."""
    step = _validate_release_tag_step()

    assert "[[ ! \"$TAG\" =~ ^v[0-9]+[.][0-9]+[.][0-9]+$ ]]" in step
