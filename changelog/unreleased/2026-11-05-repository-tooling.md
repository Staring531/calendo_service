# Repository checks, CI, release workflow and contributor conventions

- **Date:** 2026-11-05
- **Type:** process
- **Scope:** `tooling`, `ci`, `release`, `docs`, `skills`

[中文版](2026-11-05-repository-tooling.zh.md)

The repository gained a Python engineering baseline, a CI workflow with one required check, a
tag-driven release workflow, bilingual changelog and RFC formats that a script checks, and a dev
skill for coding agents. No product behaviour shipped: `src/calendo/` holds only the package and
its version.

## Engineering baseline

- `pyproject.toml` declared the `calendo` package (Python 3.12 or later, built with `uv_build`) and
  pinned the development tools in `uv.lock`: ruff 0.17.3, pyright 1.1.414 with a bundled Node,
  pytest 9.2.0, pytest-socket 0.8.1, pytest-cov 7.1.0 and actionlint-py 1.7.12.
- pytest ran with sockets disabled, strict markers and config, and warnings as errors; pyright ran
  in strict mode over `src/`, `scripts/` and `tests/`.
- `scripts/check.sh` ran the CI chain locally: `uv lock --check`, ruff format and lint, actionlint,
  the changelog and RFC checks, pyright and pytest.
- The MIT `LICENSE` from the repository's first commit was restored, and `.gitattributes` fixed
  line endings to LF.

## CI and release

- `.github/workflows/ci.yml` ran `style`, `typecheck`, `test` (Python 3.12 and 3.14), `package` and
  `records` on every pull request and push to `main`, and an aggregate `ci` job that failed unless
  every other job succeeded.
- `package` built the sdist and wheel, checked that the wheel carried `calendo/py.typed` and
  `LICENSE`, and that the installed wheel reported the version `pyproject.toml` declared.
- `records` required an entry pair under `changelog/unreleased/` on pull requests not labelled
  `skip-changelog`, and a raised version on any landed RFC that changed.
- `.github/workflows/release.yml` ran on `v*` tags: `scripts/check_release.py` on the tag's tree,
  then the full CI on the tag, then `uv build` and a GitHub Release with
  `changelog/<version>/RELEASE.md` as its body and the sdist, wheel and `SHA256SUMS` as assets. A
  tag whose Release already existed published nothing.
- Dependabot opened weekly grouped updates for GitHub Actions and uv, labelled `dependencies` and
  `skip-changelog`, and ignored `holidays`.

## Records

- `changelog/README.md` defined the entry pair, its metadata block and the types `feature`, `fix`,
  `refactor`, `data` and `process`; `scripts/check_changelog.py` checked it.
- `rfcs/README.md` and the templates defined the CRFC pair and its statuses;
  `scripts/check_rfcs.py` checked it.
- `scripts/check_release.py` refused a tag whose version, release folder, `RELEASE.md` or
  `CHANGELOG` line was not ready, or that left entries in `changelog/unreleased/`.
- `tests/tooling/` covered the three checks with 47 tests.

## Contributors and agents

- `.github/CONTRIBUTING.md`, `.github/SECURITY.md` and their Chinese counterparts replaced
  `.github/README.md`. The pull request template and the bug, feature and investigation forms were
  rewritten, and a data form for wrong dates was added.
- `AGENTS.md` and `.agents/skills/calendo-dev/` recorded the conventions for coding agents, with
  `.claude` linking to `.agents`.
- `docs/product/calendo-mvp.zh.md` carried the product background converted from the `.docx`,
  which moved beside it. The two process documents written for memrepo were removed.
