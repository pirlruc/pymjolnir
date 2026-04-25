# Improvements

## Tracking

### High Priority

- [x] **Resolve license metadata warning before publishing** — implemented with modern SPDX package
  metadata (`license = "MIT"` and `license-files = ["LICENSE"]`); `uv build` now succeeds without
  the setuptools deprecation warning.

### Medium Priority

- [x] **Update README setup command to match locked uv workflow** — release setup now uses
  `uv sync --frozen --extra dev`.
- [x] **Decide whether release builds must lock build backend versions** — kept build backend
  versions as lower-bounded requirements, but raised them to modern metadata-capable minimums
  (`setuptools>=77`, `wheel>=0.45`). Exact build-backend pinning is intentionally not used for this
  library template.
- [ ] **Verify Dependabot `uv` behavior on the first PR** — not implemented locally; requires the
  first Dependabot PR after GitHub processes `.github/dependabot.yml`.
- [ ] **Review Node 24 force flag after action upgrades** — not implemented yet; keep until all
  referenced actions, especially `gitleaks/gitleaks-action`, declare Node 24 natively.
- [ ] **Configure PyPI Trusted Publishing before first publish** — new suggestion; must be completed
  in PyPI project settings, not in repository files.

### Low Priority

- [x] **Remove deprecated `check-docstring-first` hook** — removed from `.pre-commit-config.yaml`.
- [x] **Keep and wire Pylint** — Pylint remains in the dev extra, has minimal `pyproject.toml`
  configuration, and runs in CI.
- [x] **Add project classifiers, keywords, and URLs before publishing** — added PyPI-facing
  classifiers, keywords, and project URLs.
- [x] **Add `python.analysis.typeCheckingMode`** — set to `basic` in `.vscode/settings.json`.
- [x] **Add package docs structure when APIs begin** — added `docs/README.md` as a placeholder.
- [ ] **Add coverage reporting once tests become meaningful** — new suggestion; defer until real
  library behavior exists.
- [ ] **Add CodeQL or another code-scanning workflow once implementation begins** — new suggestion;
  defer until there is substantive code to scan.

## Review Notes

Final-pass review scope: all files returned by `git ls-files --cached --others --exclude-standard`.

Validation run:

- `uv lock --check`
- `uv sync --frozen --extra dev`
- `uv run pre-commit run --all-files`
- `uv run ruff check src tests`
- `uv run ruff format --check src tests`
- `uv run mypy -p pymjolnir -p tests`
- `uv run pytest -q`
- `uv run bandit -c pyproject.toml -r src -q`
- `uv audit --preview-features audit`
- `uv build`

Result: all checks passed and `uv audit` found no known vulnerabilities. The original license
metadata warning has been resolved.

## High Priority

### Resolve license metadata warning before publishing

Original finding: `uv build` succeeded, but modern `setuptools` emitted a deprecation warning for:

```toml
license = { text = "MIT" }
```

The warning says `project.license` as a TOML table will stop being supported by `setuptools` after
2027-02-18, and recommends a SPDX string plus optional `license-files`.

Implemented:

```toml
license = "MIT"
license-files = ["LICENSE"]
```

## Medium Priority

### Update README setup command to match locked uv workflow

Original finding: `README.md` suggested `pip install -e ".[dev]"` for release preparation. The rest
of the repository uses lockfile-based installs:

```shell
uv sync --frozen --extra dev
```

Implemented: README now uses `uv sync --frozen --extra dev`.

### Decide whether release builds must lock build backend versions

CI, release, devcontainer, and publish workflows use `uv sync --frozen --extra dev`, which locks the
application/dev environment. `uv build` still uses the `[build-system]` requirements:

```toml
requires = ["setuptools>=77", "wheel>=0.45"]
```

Implemented decision: keep lower bounds rather than exact pins, because this is a library template
and Dependabot should be able to move the backend forward. The minimum was raised so modern license
metadata is supported.

### Verify Dependabot `uv` behavior on the first PR

`.github/dependabot.yml` uses the `uv` ecosystem, which is the right target for `pyproject.toml` /
`uv.lock` as of current GitHub support. Because this support is newer than `pip` / `github-actions`
/ `pre-commit`, verify the first Dependabot PR updates both metadata and lockfile as expected.

Recommended next step: if Dependabot does not update `uv.lock` correctly, switch the Python
dependency updates to a supported fallback strategy and keep `uv lock` in CI.

### Review Node 24 force flag after action upgrades

Workflows set:

```yaml
FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true
```

This is appropriate while actions such as `gitleaks/gitleaks-action` still declare Node 20. Once all
referenced actions declare Node 24 natively, the force flag can be removed to reduce
workflow-specific compatibility behavior.

### Configure PyPI Trusted Publishing before first publish

The publish workflow is ready for Trusted Publishing (`id-token: write`), but PyPI must be
configured out of band for repository `pirlruc/pymjolnir` and workflow
`.github/workflows/publish-pypi.yml`.

## Low Priority

### Remove deprecated `check-docstring-first` hook

Implemented: removed from `.pre-commit-config.yaml`.

### Decide whether `pylint` should be kept

Implemented: Pylint stays in the `dev` extra, has minimal configuration in `pyproject.toml`, and
runs in CI.

### Add project classifiers and URLs before publishing

Implemented: added:

- `classifiers`
- `keywords`
- `urls` (`Repository`, `Issues`, `Changelog`)

### Add `python.analysis.typeCheckingMode` if Pylance should enforce typing in-editor

Implemented:

```json
"python.analysis.typeCheckingMode": "basic"
```

`mypy` remains the source of truth in CI; Pylance now provides basic in-editor feedback.

### Add package docs structure when APIs begin

Implemented initial structure: added `docs/README.md`. Once design-pattern modules are added, expand
it with:

- `docs/` or `mkdocs.yml`
- examples for each pattern
- README API overview
- tests aligned to each public pattern implementation

### Add coverage reporting once tests become meaningful

The project has a smoke test only. Add coverage reporting once real behavior exists, for example by
running `coverage run -m pytest` and publishing coverage XML from CI.

### Add CodeQL or another code-scanning workflow once implementation begins

Bandit, Semgrep, Gitleaks, and uv audit already cover a good template baseline. Add CodeQL (or a
similar scanner) once there is substantive Python code and public APIs to analyze.
