# A pull request must close one adopted leaf issue

- **Date:** 2026-11-06
- **Type:** process
- **Scope:** `ci`, `docs`, `tooling`
- **PR:** [#12](https://github.com/Staring531/calendo_service/pull/12)
- **Issue:** [#11](https://github.com/Staring531/calendo_service/issues/11), [#13](https://github.com/Staring531/calendo_service/issues/13)

[中文版](2026-11-06-adopted-leaf-issue.zh.md)

A pull request now has to close one issue the owner opened or adopted, and that issue cannot still have an open sub-issue. Project cards move from those events.

## Details

- `scripts/check_requirement.py` runs in the `records` job. The owner is `Staring531`. Adoption is a comment line whose only text is `Adopted`. Labels `skip-changelog` and `dependencies` skip the check.
- A request one pull request cannot deliver stays a parent issue. The agent opens one sub-issue per story. The parent is not the issue a pull request closes while a child is open.
- `.github/workflows/project-status.yml` sets Designing for an RFC pull request, Ready for the owner's `Adopted` line, Verifying for an implementation pull request, and Done when the issue closes. The workflow reads `PROJECT_TOKEN` and does not use the app token.
- The requirement, the `Adopted` line, and the parent/child split are in `AGENTS.md` and both contributor guides. The feature form says a large request becomes a parent and makes the completion checks required.
- `docs/github/configuration.md` records the ruleset `project-main`, the five project statuses, the built-in project workflows, and the trigger of each Actions workflow. The contributor guide now points at that page and requires one approving review.
- The same page records how a topic is cut into stories: four statements, the cases that stay a parent, and a seven-tool worked cut. `AGENTS.md` lists the seven steps.
