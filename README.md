# pymjolnir

Design patterns Python library

## Releases (local Commitizen)

Releases are driven from your machine, not by automated bump jobs on GitHub.

1. On a branch that is ready to release (usually `main` after merging), install dev tools:
   `pip install -e ".[dev]"` (or your usual `uv` equivalent).
2. Run **`cz bump`**. [Commitizen](https://github.com/commitizen-tools/commitizen) updates
   `pyproject.toml` / `CHANGELOG.md` and creates a **semver tag** (e.g. `v0.2.0`) per
   `[tool.commitizen]` in `pyproject.toml`.
3. Push commits and the new tag: **`git push`** and **`git push origin vX.Y.Z`**.
4. GitHub runs **`.github/workflows/release.yml`** on the tag and creates a **GitHub Release** with
   the built sdist/wheel.
5. To publish that tag to **PyPI**, run the manual workflow **Publish to PyPI** (see
   `.github/workflows/publish-pypi.yml`) and enter the same tag. Configure **Trusted Publishing** on
   PyPI for that workflow first.
