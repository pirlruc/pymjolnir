# Agent handover log (pymjolnir)

Purpose: Continuity for humans and AI agents working on this repository—what was reviewed, decided,
changed, and what should happen next.

## How to update this file

After any **user-requested** change or substantive **repository action** (new config, dependency,
layout, CI, release prep, etc.), append a new entry under **Log entries** (newest first). Each entry
should include:

1. **Date** (ISO-8601, UTC or local—state which).
2. **Trigger** (short quote or paraphrase of the request).
3. **Actions** (files created/edited/deleted; commands run if relevant).
4. **Outcome** (what works now, what was deferred).
5. **Follow-ups** (optional bullets for the next agent).

Do not log purely informational chat with no repo impact unless the user asks to record it.

______________________________________________________________________

## Log entries (newest first)

### 2026-04-26 (local) — Exclude Dependabot config from yamlfix

**Trigger:** Keep **`.github/dependabot.yml`** schedule **`time`** values quoted after yaml
formatting.

**Actions:** Added a **`yamlfix`** hook **`exclude`** for **`.github/dependabot.yml`**, with an
inline comment explaining Dependabot requires **`schedule.time`** to remain quoted strings and
**`yamlfix`** removes those quotes.

**Outcome:** Future pre-commit runs should not rewrite Dependabot schedule times into schema-invalid
YAML integers.

### 2026-04-26 (local) — Fix Dependabot schedule time types

**Trigger:** Dependabot rejected **`.github/dependabot.yml`** because schedule **`time`** values
were parsed as YAML integers instead of strings.

**Actions:** Quoted all Dependabot schedule times: **`"06:00"`**, **`"06:15"`**, and **`"06:30"`**.

**Outcome:** Dependabot schedule values now conform to the schema’s string type.

### 2026-04-25 (local) — Clarify Dependabot metadata workflow skip behavior

**Trigger:** Dependabot metadata workflow appeared skipped on a maintainer-authored pull request;
make Dependabot-only behavior explicit.

**Actions:** Renamed workflow to **`Dependabot Metadata (Dependabot PRs only)`**, added job name
**`Summarize Dependabot dependency update`**, and added a workflow comment explaining that
maintainer-authored PRs intentionally skip because of **`github.actor == 'dependabot[bot]'`**.

**Outcome:** GitHub Actions UI should make it clearer that skipped metadata runs are expected for
non-Dependabot PRs.

### 2026-04-25 (local) — Align Ruff pre-commit hook with uv.lock

**Trigger:** Copilot review noted Ruff version drift: **`uv.lock`** resolved **`ruff==0.15.11`** but
**`ruff-pre-commit`** was pinned at **`v0.15.5`**.

**Actions:** Verified **`astral-sh/ruff-pre-commit`** tag **`v0.15.11`** exists and updated
**`.pre-commit-config.yaml`** to use it.

**Outcome:** Pre-commit Ruff and CI/local **`uv run ruff`** now use matching Ruff versions.

### 2026-04-25 (local) — Qodo review fixes for PyPI tag safety and typed package data

**Trigger:** Qodo review noted that **`publish-pypi.yml`** could checkout arbitrary refs via manual
**`tag`** input, and **`py.typed`** inclusion was not explicit in setuptools config.

**Actions:** Updated **`.github/workflows/publish-pypi.yml`** to checkout
**`refs/tags/${{ inputs.tag }}`** and validate the tag matches **`vX.Y.Z`** before publishing. Added
**`[tool.setuptools.package-data] pymjolnir = ["py.typed"]`** to **`pyproject.toml`**.

**Outcome:** Manual PyPI publish is constrained to release tags, and typed-package marker inclusion
is explicit. Verified **pre-commit**, **uv build**, and wheel contents include
**`pymjolnir/py.typed`**.

### 2026-04-25 (local) — Resolve improvements tracker items

**Trigger:** Resolve items from **`improvements.md`**, keep Pylint, and add implementation status
tracking by priority.

**Actions:** Updated **`improvements.md`** with a top-level tracking section split into high,
medium, and low priority. Resolved local items: modern SPDX license metadata, **`license-files`**,
raised build backend minimums, README locked **uv** setup command, removed deprecated
**`check-docstring-first`**, kept and wired **Pylint** into **`pyproject.toml`** and CI, added
PyPI-facing metadata, enabled Pylance basic type checking, and added **`docs/README.md`**.

**Outcome:** Local improvements are implemented; externally dependent items remain tracked (first
Dependabot `uv` PR verification, Node 24 force flag removal when upstream catches up, PyPI Trusted
Publishing setup).

### 2026-04-25 (local) — Final repository pass and improvements list

**Trigger:** Review all unignored repository files for correctness / completeness and create
**`improvements.md`** with prioritized findings.

**Actions:** Ran a full local validation pass: **`uv lock --check`**,
**`uv sync --frozen --extra dev`**, **`uv run pre-commit run --all-files`**, **ruff**, **mypy**,
**pytest**, **bandit**, **`uv audit --preview-features audit`**, and **`uv build`**. Added
**`improvements.md`** with high, medium, and low priority items.

**Outcome:** Checks pass and audit is clean. Noted one high-priority release-readiness issue: modern
**setuptools** warns that **`project.license`** as a table is deprecated; see **`improvements.md`**.

### 2026-04-25 (local) — Dependabot updates for uv, Actions, and pre-commit

**Trigger:** Add Dependabot configuration and workflow to check versions in **`pyproject.toml`** /
**`uv.lock`**, GitHub Actions YAML files, and **`.pre-commit-config.yaml`** hooks.

**Actions:** Added **`.github/dependabot.yml`** with weekly **`uv`**, **`github-actions`**, and
**`pre-commit`** update checks, grouped by ecosystem. Added
**`.github/workflows/dependabot-metadata.yml`** using **`dependabot/fetch-metadata@v3.1.0`** to
summarize Dependabot PR metadata without auto-merging or approving.

**Outcome:** Dependabot can open version update PRs for project dependencies / lockfile, workflow
actions, and pre-commit hook revisions; Dependabot PRs get a concise metadata summary in the job
summary.

### 2026-04-20 (local) — Python interpreter in workspace settings

**Trigger:** Configure the virtualenv interpreter in **`.vscode/settings.json`** instead of
**`.devcontainer/devcontainer.json`**.

**Actions:** Removed **`customizations.vscode.settings`** from
**`.devcontainer/devcontainer.json`**. Set **`python.defaultInterpreterPath`** to
**`${workspaceFolder}/.venv/bin/python`** in **`.vscode/settings.json`** (next to existing Python /
terminal settings).

**Outcome:** Dev container and local VS Code both pick up the same workspace setting for
**`uv sync`**’s **`.venv`**.

### 2026-04-20 (local) — Lockfile-based uv sync, PEP 621 license, mypy pin

**Trigger:** Copilot-style review: use **`uv.lock`** in CI/release/devcontainer/PyPI prep;
**`license`** as PEP 621 table; align **pre-commit mypy** with lockfile **mypy** version.

**Actions:** **CI** / **release** / **publish-pypi**: replace **`uv pip install -e ".[dev]"`** with
**`uv sync --frozen --extra dev`**. **devcontainer**: **`uv sync --frozen --extra dev`** and
**`uv run pre-commit install`**. **`pyproject.toml`**: **`license = { text = "MIT" }`**;
**`mypy>=1.20.1`** in **`dev`**. **`.pre-commit-config.yaml`**: **`mirrors-mypy`**
**`rev: v1.20.1`** (matches **`uv.lock`**); ran **`uv lock`** if metadata changed. (Interpreter path
later moved to **`.vscode/settings.json`** — see newer handover entry.)

**Outcome:** Reproducible installs from **`uv.lock`**; mypy versions aligned between pre-commit and
**`uv run mypy`**.

### 2026-04-20 (local) — GitHub Actions Node 20 deprecation warnings

**Trigger:** CI warned that Node.js 20–based actions are deprecated (`checkout`, `setup-python`,
`setup-uv`, `gitleaks-action`).

**Actions:** Bumped **`actions/checkout@v6`**, **`actions/setup-python@v6`**,
**`astral-sh/setup-uv@v8`**, **`softprops/action-gh-release@v3`**; pinned
**`gitleaks/gitleaks-action@v2.3.9`**; set workflow-level
**`FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true`** on **CI**, **Release**, and **Publish to PyPI** so
actions still declaring Node 20 (e.g. Gitleaks) run on Node 24 per GitHub guidance.

**Outcome:** Aligns with the Node 24 migration; revisit **`gitleaks-action`** when a release ships
**`runs.using: node24`**, then the force flag can be dropped if you want.

### 2026-04-20 (local) — pre-commit name-tests-test vs pytest file names

**Trigger:** `name-tests-test` failed: `tests/test_pymjolnir.py` did not match `.*_test\.py`.

**Actions:** **`.pre-commit-config.yaml`**: set **`args: [--pytest-test-first]`** on
**`name-tests-test`** so names must match **`test_.*\.py`** (pytest convention).

**Outcome:** `tests/test_pymjolnir.py` passes the hook.

### 2026-04-20 (local) — Document Option A releases (local Commitizen)

**Trigger:** Adopt Option A for commit / release workflow (local Commitizen, not server-automated
bumps).

**Actions:** **`README.md`**: “Releases (Option A — local Commitizen)” with `cz bump` → push tag →
`release.yml` → manual **Publish to PyPI**. **`.github/workflows/release.yml`**: header comments
aligned. **`pyproject.toml`**: one-line note above **`[tool.commitizen]`**.

**Outcome:** Single documented path for maintainers; matches existing GitHub workflows.

### 2026-04-20 (local) — CI triggers, manual PyPI, gitleaks guard, uv audit notes

**Trigger:** CI on feature branches + `main` (drop `master`); PyPI only via `workflow_dispatch`;
same-repo gitleaks; clarify commit workflows; keep `v*.*.*` releases; keep `uv audit`.

**Actions:**

- **`.github/workflows/ci.yml`**: `push` on all **`branches: ["**"]`** (excludes tag pushes);
  **`pull_request`** targeting **`main`** only; removed **`master`**; **Gitleaks** step **`if:`**
  skips fork PRs; **`uv audit`** comment retained with **`--preview-features audit`**.
- **`.github/workflows/publish-pypi.yml`**: new **manual** PyPI publish on **`workflow_dispatch`**
  with **`tag`** input; **`id-token: write`** for **Trusted Publishing**;
  **`pypa/gh-action-pypi-publish`** + **`attestations: true`**.
- **`.github/workflows/release.yml`**: docstring points to **`publish-pypi.yml`**; removed commented
  inline PyPI step.

**Outcome:** Branch pushes and PRs into `main` run CI; PyPI is explicit human-triggered; OIDC-ready
publish workflow.

### 2026-04-20 (local) — Typos, GitHub Actions (CI + release), Commitizen

**Trigger:** Add typo checking for README and docstrings; GitHub Actions for ruff, mypy, pytest,
bandit, gitleaks, uv audit, uv build; release workflow with Commitizen-oriented tagging; collect
open questions for maintainers.

**Actions:**

- Chose **typos** (`crate-ci/typos`, pre-commit `v1.45.1`) over codespell: fast, `typos.toml`
  config, good defaults for prose + code identifiers.
- Added **`typos.toml`**, **`tests/test_pymjolnir.py`**, **`src/pymjolnir/py.typed`**,
  **`CHANGELOG.md`**, **`.github/workflows/ci.yml`**, **`.github/workflows/release.yml`**.
- **`pyproject.toml`**: **`bandit[toml]`** and **`commitizen`** in **`dev`**;
  **`[tool.commitizen]`** (`version_provider = "pep621"`); **`[tool.bandit]`**;
  **`mypy_path = ["src"]`**; **`license = "MIT"`** (SPDX string); mypy invocation uses
  **`-p pymjolnir -p tests`** (avoids duplicate-module noise with editable installs).
- **`.pre-commit-config.yaml`**: typos hook; mypy args aligned with CI.
- **CI**: `uv venv` + **`uv pip install -e ".[dev]"`**, ruff, mypy, pytest, bandit,
  **gitleaks/gitleaks-action@v2**, **`uv audit --preview-features audit`**, **`uv build`**.
- **Release**: on **`v*.*.*`** tags, **`uv build`** + **softprops/action-gh-release** with
  **`dist/*`**; PyPI publish left commented with **`pypa/gh-action-pypi-publish`**.

**Outcome:** Local + CI typo checks; unified quality/security/build pipeline; tag-driven GitHub
releases with artifacts.

**Follow-ups / questions for you:** See the assistant’s latest reply (default branch name, PyPI
publishing, gitleaks on fork PRs, Commitizen bump workflow, `uv audit` preview flag).

### 2026-04-20 (local) — Ruff on save, JSON excludes, EditorConfig indent, Pydantic + mypy

**Trigger:** Run Ruff organize imports and fix-all on save; remove JSONC comment from
`settings.json` and narrow pre-commit JSON excludes; align JSON EditorConfig indent with preference
for 4 spaces; add Pydantic mypy plugin in `pyproject.toml` and pre-commit mypy env; optional tooling
suggestions.

**Actions:**

- `.vscode/settings.json`: set `source.organizeImports.ruff` and `source.fixAll.ruff` to
  **`always`**; removed the explanatory comment (file is strict JSON again).
- `.pre-commit-config.yaml`: `check-json` / `format-json` exclude list no longer includes
  `.vscode/settings.json`; mypy hook **`additional_dependencies: [pydantic>=2.0]`** so
  `pydantic.mypy` loads in the hook environment.
- `.editorconfig`: **`[*.json]`** / **`[*.jsonc]`** `indent_size` set from **2 → 4** (matches global
  Python-oriented preference; YAML stays at 2).
- `pyproject.toml`: **`plugins = ["pydantic.mypy"]`**, **`[tool.pydantic-mypy]`** defaults,
  **`pydantic>=2.0`** in **`dev`** optional dependencies.

**Outcome:** Save triggers Ruff import organization and fixes; mypy + Pydantic plugin configured
consistently for local `dev` installs and pre-commit’s isolated mypy.

**Follow-ups:** If the library never uses Pydantic at runtime, keep it in **`dev`** only (current);
if you add runtime Pydantic models, move **`pydantic`** to **`[project].dependencies`**. Consider
**`typos`**, **`check-shebang-scripts-are-executable`**, and a **`commitizen`** or **`tbump`**
workflow when you start versioning releases.

### 2026-04-20 (local) — Handover rename, Ruff docstrings, uv devcontainer, housekeeping

**Trigger:** Rename handoff log to `agent-handover.md`; align EditorConfig, pre-commit,
devcontainer, VS Code settings, and `.gitignore` per latest review; add `pyproject.toml` template
and packaging skeleton; clarify Ruff vs docstring tools in chat (see entry below for rationale).

**Actions:**

- Renamed handoff log from `AGENT_HANDOFF_LOG.md` to `agent-handover.md` (this file); removed
  `AGENT_HANDOFF_LOG.md`.
- Updated `.cursor/rules/agent-handoff-log.mdc` to reference `agent-handover.md`.
- `.editorconfig`: `[Makefile]` (tabs); `[*.json]` / `[*.jsonc]` (2-space indent).
- `.pre-commit-config.yaml`: removed Flake8, `format-docstring`, `docformatter`, `pydoclint`; set
  `pyupgrade` to `--py313-plus`; tightened mypy hook (`--config-file=pyproject.toml`, `src`,
  `pass_filenames: false`, `always_run: true`); Semgrep args set to `p/python` with comment;
  excluded `.vscode/settings.json` from strict `check-json` / `format-json` (file uses JSONC
  comments).
- Added `pyproject.toml` (setuptools `src/` layout, `[tool.ruff]`, `[tool.mypy]`, `dev` optional
  deps) and `src/pymjolnir/__init__.py` so `uv pip install -e ".[dev]"` is valid.
- `.devcontainer/devcontainer.json`: `postCreateCommand` bootstraps with `pip install uv` then
  `uv pip install --system -e ".[dev]"` and `pre-commit install`; removed `ms-python.autopep8`;
  dropped flake8 from pip installs (removed entire old multi-pip dev-tools line).
- `.vscode/settings.json`: JSONC comment explaining `explicit` vs `always` for Ruff code actions on
  save.
- `.gitignore`: `.DS_Store`.
- Added `.gitlint` (conventional-commit title contrib, line lengths, WIP guard).

**Outcome:** Single handover filename; tooling centered on Ruff + mypy template; devcontainer
installs project via `uv`; Semgrep uses a pinned community ruleset instead of `auto`.

**Follow-ups:** If Conventional Commits are too strict, relax or remove
`contrib-title-conventional-commits` in `.gitlint`. If Semgrep `p/python` is too narrow or too
broad, switch to a custom `semgrep.yml` or CI-only Semgrep. Consider `uv sync` + lockfile when you
adopt uv as the project’s primary resolver (optional).

### 2026-04-20 (local) — Configuration review, handoff log, maintenance rule

**Trigger:** Review `.editorconfig`, `.pre-commit-config.yaml`, and `.devcontainer/`; suggest
improvements; create a handoff log for another agent; add a rule to keep this log updated on future
repo changes.

**Repository state at time of entry:** No application code or `pyproject.toml`; template-only
layout. Untracked `.DS_Store` present at repo root (consider ignoring—see follow-ups).

**Reviewed:** `.editorconfig`, `.pre-commit-config.yaml`, `.devcontainer/devcontainer.json`,
`.vscode/settings.json`, `README.md`, `.gitignore` (spot-check).

**Findings (configuration review):**

| Area                 | Assessment                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **EditorConfig**     | Sensible defaults (UTF-8, LF, final newline, trim trailing space). YAML set to 2 spaces matches typical CI/config style. Markdown leaves trailing whitespace alone (good for hard line breaks). Optional later: `Makefile` tab rule; optional `[*.{json,jsonc}]` if JSONC files are edited often.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **pre-commit**       | Broad and strict for an empty repo: docstring formatters/linters, mypy, pydoclint, docstr-coverage, flake8 **and** ruff, pygrep-hooks, bandit, semgrep, gitleaks. Many hooks are valuable but **flake8 + ruff** overlap; triple docstring tooling (`format-docstring`, `docformatter`, pydoclint) can conflict—pick a primary story (often **ruff** + optional **ruff pydocstyle rules** or pydoclint alone). **mypy** with `pydantic>=2` and `--ignore-missing-imports` is fine for bootstrap but needs `pyproject.toml` `[tool.mypy]` + `packages` / `src` layout when code lands. **pyupgrade** uses `--py310-plus`\*\* while devcontainer uses **Python 3.13**—align `pyupgrade` args with `requires-python` when `pyproject.toml` exists. **gitlint** typically needs a `.gitlint` or documented commit conventions. **semgrep-ci** `--config auto` on pre-push may need network and can add latency. |
| **devcontainer**     | Image `python:3.13` matches modern stack. `postCreateCommand` as an **object** with string values is valid per devcontainers JSON schema (named lifecycle commands). Consider one `pip install` line (or a `scripts/bootstrap.sh` + `requirements-dev.txt`) instead of many separate `pip install` invocations for speed and reproducibility. **ms-python.autopep8** extension is redundant if **Ruff** is the formatter—consider removing autopep8 to avoid mixed formatting advice. When `pyproject.toml` exists, prefer `pip install -e ".[dev]"` + `pre-commit install` in `postCreateCommand`.                                                                                                                                                                                                                                                                                                        |
| **VS Code settings** | Ruff as default Python formatter matches pre-commit. `python.testing.pytestArgs`: `["tests"]` will matter once `tests/` exists; until then the UI may show no tests or warnings—expected for a template. `source.fixAll.ruff` / `organizeImports.ruff` set to **explicit** means they do not run on every save unless triggered—intentional tradeoff (fewer surprises vs more manual fixes).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **.gitignore**       | Standard Python template; **`.DS_Store` is not listed** (macOS)—easy addition.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |

**Actions taken (that session):**

- Added `AGENT_HANDOFF_LOG.md` (later renamed to `agent-handover.md`; see newer log entry).
- Added Cursor rule: `.cursor/rules/agent-handoff-log.mdc` (`alwaysApply: true`) requiring agents to
  append to the handover log after user-requested repo changes or substantive actions.

**Follow-ups (superseded or done in later entry):** Several items (pyproject, flake8 removal,
`.DS_Store`, devcontainer install path) were addressed in the **2026-04-20 — Handover rename…**
entry above.

______________________________________________________________________

_End of log at creation. Append newer entries above this line or above the previous “newest”
block—keep newest first._
