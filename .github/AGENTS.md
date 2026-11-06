# AGENTS.md

The root [AGENTS.md](../AGENTS.md) applies here too. On a conflict, this file wins for `.github/`.

## CI and release

- `.github/workflows/ci.yml` runs on every pull request and every push to `main`. The ruleset
  `project-main` on the default branch requires a pull request, one approving review, and the
  aggregate `ci` job. `ci` fails unless `style`, `typecheck`, `test`, `package` and `records`
  all succeeded, so a skipped or cancelled job is not a pass.
- `records` runs its checks on pull requests only. It requires a changelog pair and exactly one
  closed issue that the owner opened or adopted and that has no open sub-issues.
  `skip-changelog` skips the changelog pair and that issue check. `dependencies` skips the issue
  check. Adding or removing either label re-runs the workflow.
- `.github/workflows/project-status.yml` moves the project card: an RFC pull request to
  Designing, an `Adopted` comment by the owner to Ready, an implementation pull request to
  Verifying, and a closed issue to Done. It uses the `PROJECT_TOKEN` secret. The app token does
  not edit the project.
- Tests run on Python 3.12 and 3.14 with sockets disabled. There is no coverage threshold.
- A pushed tag is never moved. Release preparation is its own pull request. The order and the
  `RELEASE.md` shape are in
  [`.agents/skills/calendo-dev/reference/release.md`](../.agents/skills/calendo-dev/reference/release.md).
  Cutting the release or pushing the tag is the owner's call.
- Workflow permissions stay read-only unless a job asks for what it needs. The release job asks
  for `contents: write`.
- A vulnerability is reported through the private advisory form in [`SECURITY.md`](SECURITY.md),
  not a public issue.
