# Verification

Loaded on demand from `SKILL.md`: what to run for what you changed, and how a check can pass
without proving anything.

## What to run

`uv sync` first in a fresh checkout. The full chain is `sh scripts/check.sh`, the same commands CI
runs. While you work, pick the narrowest evidence that would fail for this change's regression:

| Changed | Run |
| --- | --- |
| Markdown only: README, docs, `.agents/`, `.github/*.md` | `git diff --check`, and read it as a reader would (`writing.md`) |
| A changelog entry | `uv run python scripts/check_changelog.py` |
| An RFC | `uv run python scripts/check_rfcs.py --base origin/main` |
| `src/calendo/**` | the tests for that module, then `uv run pyright` and `uv run pytest` |
| A date fact, a fixture, the `holidays` pin | `uv run pytest`, plus the list of every date whose answer moved, in the PR body |
| `scripts/**` | `uv run pytest tests/tooling` and `uv run pyright` |
| `.github/workflows/**`, `.github/actions/**` | `uv run actionlint`; `uv run --with shellcheck-py actionlint` also runs the shellcheck pass CI's runner has |
| `pyproject.toml`, `uv.lock` | `uv lock --check`, then the full chain |
| The release path | `uv run python scripts/check_release.py --tag v<version>` on the release branch |

Always cheap, always worth it: `git diff --check`, and `uv run ruff format .` on any Python diff.

## Two ways a test proves nothing

**An assertion that was already true at the base commit is not a test of the change.** Check a new
test against the code before your change (`git stash`, run, `git stash pop`); keep the assertions
that fail there.

**An expectation computed by the code under test proves only that the code agrees with itself.**
A date fact's expected value comes from a fixture or a labelled observation, never from calling
the function being tested.

## Reading CI without fooling yourself

- **The required check is `ci`**, the aggregate. It fails on any job that did not succeed, so a
  skipped or cancelled job cannot read as green. Read its log when a run looks too fast.
- **A queued run has registered no checks**, so "no check is failing" is trivially true in the
  first seconds after a push. Poll the run (`gh run list --branch <branch> --limit 1`), not the
  checks.
- **A conflicting pull request runs no checks at all**: GitHub builds no merge commit while the
  branch conflicts with `main`. Merge `origin/main` in, resolve, push, then expect checks.
- **A piped command reports the pipe's exit code.** `uv run pytest | tail` succeeds when the tests
  fail. Check the real output, or `set -o pipefail`.
- **A machine difference is a finding.** A test that passes here and fails in CI has caught an
  environment assumption (a locale, a timezone, a Python version). Fix the assumption; do not
  pin the environment to make it green.
