# Writing tests: scenarios first, behaviour only

Loaded on demand from `SKILL.md`. A test earns its place by failing when a promise to a caller
breaks, and by staying green through a refactor that keeps the promise. "2025-10-11 in CN is an
adjusted workday" is a test. "`DEFAULT_LANG` equals `zh_CN`" is not: it restates the source and
fails on every legitimate edit.

## 1. Scenarios before code

Before writing a test module, write its scenarios in the module docstring, in plain words, each a
behaviour somebody depends on:

```python
"""Working days in a range, as an agent asks count_workdays.

- Given 2025-09-29 to 2025-10-12 in CN, the count includes both ends.
- Given a range whose end is before its start, the answer is the error invalid_range, and
  nothing is counted.
- Given a year outside the allowed years, the answer is year_not_supported, never an empty count.
"""
```

- One test function per scenario, named as the behaviour:
  `test_a_range_includes_both_of_its_ends`. A reviewer must be able to judge coverage from the
  docstring and the names alone.
- Arrange and assert through the surface the caller has: a core function, an HTTP request, an MCP
  tool call. Assert what that caller can observe: the returned fields, the error code, the status.
- Look first for what must **not** happen: an unsupported year must not come back as an empty
  list, an unverified answer must not read as official, a request must not touch the network.
- Parametrize one behaviour over its cases with `pytest.mark.parametrize`, not by copying tests.

## 2. Date expectations carry their source

Every expected date fact in a test comes from one of two places, and the test says which:

- **An official fixture**: the expectation is read from the fixture file, which links the notice.
  These tests decide `official`.
- **An observation of the library** at its pinned version: the test pins what `holidays` does so
  that an upgrade that changes it fails loudly. Its name or docstring says it is an observation,
  e.g. `test_observed_nth_working_day_from_a_non_working_day_treats_0_and_1_alike`. An observation
  is never presented as a verified answer.

A test never computes its expectation with the code under test, and never types a date fact into
an assertion without one of those two sources behind it.

## 3. What never earns a test

- Constants and tables restated: a default language, a list of supported countries copied from
  the source. Test the behaviour the value drives.
- Implementation mirrors: which private helper ran, how many times, the shape of an intermediate
  object.
- Copy snapshots: a tool description or an error message compared to the string in the source.
  The exception is text a caller acts on — an error that tells the model how to fix its request —
  and then the test asserts that the error reaches the caller when the case happens.
- Anything this repository does not pin: the network, today's date, another repository's branch.
  Pass dates in explicitly; a function that needs "today" takes it as an argument or a clock.
- The same scenario at two layers. Keep the one closest to the caller, unless the lower one
  reaches branches the upper cannot reach cheaply.

## 4. Where the fakes go

| Boundary | How |
| --- | --- |
| The network | Disabled for every test by pytest-socket. Nothing fakes it, because the service never uses it. |
| `holidays` | Not faked. It is pinned, local and deterministic; tests call the real library. |
| Time | An explicit date argument or an injected clock. Never the system clock. |
| Filesystem | `tmp_path`. Do not mock `pathlib` or `open`. |
| Processes | Spawn only when the process is the behaviour (the tooling tests run real `git`). |
| Our own modules | Never `monkeypatch`ed to fake another of our modules. If a test needs that, the seam is wrong. |

## 5. Coverage and speed

- CI measures branch coverage. Every branch a change adds is taken by a scenario, both ways where
  both are behaviour. A change that deletes tests does not lower branch coverage; say before and
  after in the PR body when you prune.
- There is no threshold. A test written only to colour a line, asserting nothing a caller depends
  on, is junk from §3.
- Keep each test well under a second. No sleeps, no servers per test; share setup through a
  module- or session-scoped fixture when the scenarios read and do not mutate.

## Checklist

- [ ] The scenarios are in the module docstring; each test name is a behaviour.
- [ ] Every assertion is observable by the caller; nothing restates a constant or the source.
- [ ] Every expected date fact names its source: an official fixture, or a labelled observation.
- [ ] Nothing reads the network, the system clock or another repository.
- [ ] The branches the change adds are taken; pruning did not lower branch coverage.
