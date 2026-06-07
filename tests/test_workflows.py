"""Regression tests for GitHub Actions workflow safety invariants."""

import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PUBLISH_PYPI_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "publish-pypi.yml"


def _workflow_step(workflow: str, step_name: str, next_step_name: str | None = None) -> str:
    """Return the text for a named workflow step."""
    step_start = workflow.index(f"      - name: {step_name}\n")
    if next_step_name is None:
        return workflow[step_start:]

    step_end = workflow.index(f"      - name: {next_step_name}\n", step_start)
    return workflow[step_start:step_end]


def _literal_run_script(step: str) -> str:
    """Return the script body from a literal block `run: |` workflow step."""
    run_marker = "        run: |\n"
    run_start = step.index(run_marker) + len(run_marker)
    script_lines: list[str] = []

    for line in step[run_start:].splitlines():
        if line.startswith("          "):
            script_lines.append(line.removeprefix("          "))
            continue
        if not line:
            script_lines.append("")
            continue
        break

    return "\n".join(script_lines)


def test_publish_pypi_tag_input_is_validated_before_checkout() -> None:
    """The manual publish workflow must reject unsafe tag input before checkout."""
    workflow = PUBLISH_PYPI_WORKFLOW.read_text(encoding="utf-8")

    validate_start = workflow.index("      - name: Validate release tag\n")
    checkout_start = workflow.index("      - name: Checkout tag\n")
    verify_start = workflow.index("      - name: Verify release tag\n")

    assert validate_start < checkout_start < verify_start

    validate_step = _workflow_step(workflow, "Validate release tag", "Checkout tag")
    verify_step = _workflow_step(workflow, "Verify release tag", "Set up Python")

    assert "TAG: ${{ inputs.tag }}" in validate_step
    assert "TAG: ${{ inputs.tag }}" in verify_step
    assert r"^v[0-9]+\.[0-9]+\.[0-9]+$" in validate_step
    assert "${{ inputs.tag }}" not in validate_step.replace("TAG: ${{ inputs.tag }}", "")
    assert "${{ inputs.tag }}" not in verify_step.replace("TAG: ${{ inputs.tag }}", "")


def test_publish_pypi_tag_validation_rejects_command_substitution(tmp_path: Path) -> None:
    """Malicious tag text must be treated as data, not executable shell."""
    workflow = PUBLISH_PYPI_WORKFLOW.read_text(encoding="utf-8")
    validate_step = _workflow_step(workflow, "Validate release tag", "Checkout tag")
    validate_script = _literal_run_script(validate_step)

    marker = tmp_path / "command-substitution-marker"
    malicious_tag = f"v1.2.3$(printf injected >{marker})"
    env = os.environ.copy()
    env["TAG"] = malicious_tag

    result = subprocess.run(
        ["bash", "-c", validate_script],
        check=False,
        env=env,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 1
    assert "Tag must match the release pattern vX.Y.Z" in result.stderr
    assert not marker.exists()
