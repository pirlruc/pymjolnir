"""Regression tests for the manual PyPI publishing workflow."""

from pathlib import Path

WORKFLOW = Path(".github/workflows/publish-pypi.yml")


def _workflow_text() -> str:
    """Return the PyPI publishing workflow text."""
    return WORKFLOW.read_text(encoding="utf-8")


def _validate_release_tag_step() -> str:
    """Return the release-tag validation step block."""
    workflow = _workflow_text()
    start = workflow.index("      - name: Validate release tag\n")
    end = workflow.index("      - name: Checkout tag\n", start)
    return workflow[start:end]


def _validate_release_tag_run_body() -> str:
    """Return the shell body from the release-tag validation step."""
    step = _validate_release_tag_step()
    return step.split("        run: |\n", maxsplit=1)[1]


def test_publish_workflow_validates_tag_before_checkout() -> None:
    """Reject unsafe tag input before checking out attacker-controlled refs."""
    workflow = _workflow_text()

    assert workflow.index("      - name: Validate release tag\n") < workflow.index(
        "      - name: Checkout tag\n",
    )


def test_publish_workflow_passes_tag_input_through_environment() -> None:
    """Avoid direct shell interpolation of the workflow_dispatch input."""
    step = _validate_release_tag_step()
    run_body = _validate_release_tag_run_body()

    assert "TAG: ${{ inputs.tag }}" in step
    assert "${{ inputs.tag }}" not in run_body


def test_publish_workflow_rejects_non_semver_tag_names() -> None:
    """Keep tag validation strict enough to reject shell metacharacter payloads."""
    step = _validate_release_tag_step()

    assert '[[ ! "$TAG" =~ ^v[0-9]+[.][0-9]+[.][0-9]+$ ]]' in step
