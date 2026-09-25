# Agents

Use these project-specific defaults when making future changes:

- Run tests with `pytest`.
- Use `tox` to run the full test matrix across supported Python versions.
- Keep `core-requirements.txt` for runtime dependencies and `extra-test-requirements.txt` for test-only dependencies.
- Regenerate `requirements.txt` from those inputs with `tox -e compile`. Use `tox -e compile -- --upgrade` to upgrade dependencies to the latest compatible versions.
- When changing supported Python versions, keep `tox.toml`, GitHub workflows, and `setup.py` trove classifiers in sync.
- Keep `.python-version` set to the lowest supported Python version so Dependabot and single-version tooling pick it up correctly.
- Keep `base_python` in the `compile` environment in `tox.toml` set to the lowest supported Python version so that `tox -e compile` works correctly.
- When changing supported Python versions, recompile the `requirements.txt` file with `tox -e compile -- --upgrade` to ensure that compatible versions of dependencies are used.
