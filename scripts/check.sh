#!/bin/sh
# The chain CI's style, typecheck and test jobs run, in the same order, on this machine.
# A change is not ready for review until this passes.
set -eu
cd "$(dirname "$0")/.."

run() {
  printf '\n$ %s\n' "$*"
  "$@"
}

run uv lock --check
run uv run ruff format --check .
run uv run ruff check .
run uv run actionlint
run uv run python scripts/check_changelog.py
run uv run python scripts/check_rfcs.py
run uv run pyright
run uv run pytest
printf '\nEvery check passed.\n'
