# AGENTS.md

The root [AGENTS.md](../AGENTS.md) applies here too. On a conflict, this file wins for `tests/`.
Date facts the tests pin are ruled by [`src/calendo/AGENTS.md`](../src/calendo/AGENTS.md).

## What a test proves

Write the scenarios in the module docstring before the tests. One test per scenario, named as the
behaviour. Assert what a caller observes, and look first for what must not happen. Never test a
constant or restate the source.

Every expected date fact comes from a fixture that links its official source, or from a labelled
observation of `holidays` at its pinned version. A test never computes its expectation with the
code under test, and never types a date in by hand. An assertion that was already true before the
change is not a test of the change.

Sockets are disabled (pytest-socket). A test that needs the network is wrong.

The checklist is [`.agents/skills/calendo-dev/reference/testing.md`](../.agents/skills/calendo-dev/reference/testing.md).
What to run for this change is [`.agents/skills/calendo-dev/reference/verification.md`](../.agents/skills/calendo-dev/reference/verification.md).
