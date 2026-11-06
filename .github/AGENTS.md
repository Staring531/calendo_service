# AGENTS.md

The root [AGENTS.md](../AGENTS.md) applies here too. On a conflict, this file wins for `.github/`.

## CI and release

- `.github/workflows/ci.yml` runs on every pull request and every push to `main`. Branch
  protection requires the aggregate `ci` job. It fails unless `style`, `typecheck`, `test`,
  `package` and `records` all succeeded, so a skipped or cancelled job is not a pass.
- `records` runs its checks on pull requests only. `skip-changelog` exempts the changelog-entry
  check and nothing else. Adding or removing that label re-runs the workflow.
- Tests run on Python 3.12 and 3.14 with sockets disabled. There is no coverage threshold.
- A pushed tag is never moved. Release preparation is its own pull request. The order and the
  `RELEASE.md` shape are in
  [`.agents/skills/calendo-dev/reference/release.md`](../.agents/skills/calendo-dev/reference/release.md).
  Cutting the release or pushing the tag is the owner's call.
- Workflow permissions stay read-only unless a job asks for what it needs. The release job asks
  for `contents: write`.
- A vulnerability is reported through the private advisory form in [`SECURITY.md`](SECURITY.md),
  not a public issue.
