"""Regression tests for the manual PyPI publishing workflow."""

from pathlib import Path


WORKFLOW_PATH = Path(__file__).parents[1] / ".github" / "workflows" / "publish-pypi.yml"


def _publish_workflow() -> str:
    """Return the publish workflow as text."""
    return WORKFLOW_PATH.read_text(encoding="utf-8")


def test_publish_workflow_validates_tag_before_checkout() -> None:
    """Reject unsafe tag input before any ref is checked out."""
    workflow = _publish_workflow()

    assert workflow.index("- name: Validate release tag input") < workflow.index(
        "- name: Checkout tag",
    )
    assert r"^v[0-9]+\.[0-9]+\.[0-9]+$" in workflow


def test_publish_workflow_does_not_interpolate_tag_in_shell() -> None:
    """Keep workflow_dispatch input out of shell scripts."""
    workflow = _publish_workflow()

    assert 'case "${{ inputs.tag }}"' not in workflow
    assert 'refs/tags/${{ inputs.tag }}"' not in workflow
    assert "RELEASE_TAG: ${{ inputs.tag }}" in workflow


def test_publish_workflow_checks_package_version_before_publish() -> None:
    """Prevent publishing artifacts whose package version does not match the tag."""
    workflow = _publish_workflow()

    assert workflow.index("- name: Verify package version matches tag") < workflow.index(
        "- name: Build distributions",
    )
    assert 'tomllib.load(pyproject)["project"]["version"]' in workflow
