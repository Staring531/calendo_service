# GitHub settings for this repository

[中文版](configuration.zh.md)

This page records the repository rules, the user project, and the workflows read from GitHub on
2026-11-06. The ruleset, the project workflow switches, and the Actions secrets live on GitHub,
outside git history. A change to those switches updates this page in the same pull request.

## Two identities

`Staring531` is the owner. That account opens issues, writes `Adopted`, approves pull requests,
squash-merges, and owns the project.

`cursor-cf` is the GitHub App installed on this repository. An agent working in the checkout opens
pull requests with its installation token. The local `.envrc` sets `GH_TOKEN` to that token on
entering the repository, so `gh` run inside the checkout is the App. Outside the checkout, `gh`
returns to the `Staring531` login stored in the keyring.

To run `gh` as the owner from inside the checkout, drop the App token first:

```sh
env -u GH_TOKEN gh ...
```

GitHub refuses a review from the account that opened the pull request. While the agent and the
owner share `Staring531`, the commit author, the labels, and the files do not show who acted. The
App opens the pull request and the owner approves it, which is what lets the ruleset stop a direct
push to `main`.

`GET /user` with the App token returns 403 and the body `Resource not accessible by integration`.
That response means the token belongs to the App. The same token cannot write Actions secrets.
Setting `PROJECT_TOKEN` drops `GH_TOKEN` first.

## Repository and merge method

`Staring531/calendo_service` is public. On a free private repository this ruleset could not be
turned on; the API asked for GitHub Pro.

Merges are squash only. `allow_squash_merge` is true. `allow_merge_commit` and
`allow_rebase_merge` are false. One change leaves one commit on `main`, and the commit message is
the pull request title.

## Ruleset project-main

Ruleset 26674411, enforcement `active`, on the default branch. The bypass list is empty, and the
read value of `current_user_can_bypass` is `never`. Administrators do not skip the rules. The page
is https://github.com/Staring531/calendo_service/rules/26674411 .

| Rule | Parameters read | What it does | Why |
| --- | --- | --- | --- |
| `deletion` | none | `main` cannot be deleted | The default branch stays in the repository |
| `non_fast_forward` | none | `main` cannot be force-pushed, and commits already on it cannot be rewritten | Merged history stays where it landed |
| `pull_request` | 1 approving review; a new push dismisses the review; `allowed_merge_methods` is `squash` only; no code-owner review; no approval of the last push; no required thread resolution; `require_extra_approval_for_unattributed_changes` is false | A change reaches `main` through a pull request that has one Approve | The owner approves a pull request the App opened. Commits may be written by the local git user. One approval is enough |
| `required_status_checks` | the context name is exactly `ci`; `strict_required_status_checks_policy` is true, so the branch contains the latest `main`; `do_not_enforce_on_create` is false | The check named `ci` has succeeded before merge | Format, types, tests, packaging, and records are folded into the job named `ci`. The ruleset requires that one name |

## Approving and merging

1. Open the pull request. The author is `app/cursor-cf`.
2. When the state is Closed and the pull request was not merged, choose Reopen pull request.
3. Open Files changed, choose Review changes, choose Approve, then Submit review.
4. Return to Conversation. After `ci` has succeeded, the green button is Squash and merge. Choose
   it, then confirm.

A push after the approval dismisses that Approve. The pull request needs another review.

## When an issue is a requirement

A requirement is a GitHub issue in this repository. A chat message does not raise one and does not
adopt one. A file under `docs/` does not either.

An issue is adopted when either of these is true:

- `Staring531` opened it.
- `Staring531` commented a line whose text, after stripping surrounding whitespace, is exactly
  `Adopted`. Other lines in that comment do not count.

A request one pull request cannot deliver is a parent issue. The agent opens one sub-issue per
story. The parent stays open while any child is open, and the pull request closes the child. A
child waits for the same adoption before implementation starts.

On a pull request, the `records` job runs `scripts/check_requirement.py`. The body names exactly
one issue with `Closes`, `Fixes`, or `Resolves`, as a full URL:

```text
Closes https://github.com/Staring531/calendo_service/issues/N
```

That issue is adopted and has no open sub-issues. The labels `skip-changelog` and `dependencies`
skip this check. `skip-changelog` also skips the check that the branch adds a changelog pair.

The feature form requires "How to tell it is done". The form says that a request one pull request
cannot deliver becomes a parent.

An RFC with `Status: draft` is still a draft, including a draft that has been merged. It does not
authorise implementation. The owner accepts it by merging with `Status: accepted`. An agent does
not change that line. [CRFC-0001](../../rfcs/CRFC-0001-requirement-flow.md) is one such draft. This
page does not adopt its clarification record.

## Splitting a topic into stories

A topic is a parent when one pull request cannot deliver it. The agent cuts the parent into
stories, opens one sub-issue per story, and leaves the parent open. The cut follows the seven
steps in the root [`AGENTS.md`](../../AGENTS.md). This section is the standard those steps apply,
and one worked cut.

A story carries four statements:

| Statement | What it contains |
| --- | --- |
| Behaviour | The call a caller can make, and the answer or error they receive. One behaviour a caller can accept or reject on its own |
| Left out | The behaviours that stay on the parent or on a sibling, named as those issues |
| Source | For every date in the answer: the official notice and its link, the pinned `holidays` version the value was read from, or the gap |
| Checks | Questions with their right answers. Someone can mark the story done from the questions alone, without reading the code |

A cut is still a parent when any of these is true:

- The checks, the code, and the changelog do not fit in one pull request.
- A caller can use one part while another part is missing, and those parts have different checks or different date sources.
- The behaviour depends on a choice that is still open. The choice is its own RFC pull request. The story waits. The RFC and the implementation do not share a pull request.
- The story names more than one date source.

A line does not become a sub-issue when a caller cannot observe it. No new answer, no new error,
no new field, and no new documented limit means there is nothing to adopt. A rename, a file move,
or a tool bump rides inside the story that needs it.

The first story includes the code that story's one check needs. A later story names the merged
issue it depends on. There is no sub-issue whose only text is "build the core" or "set up the
framework". If that work has a checkable answer, the answer is the story. If it does not, the
work belongs inside the first story that has one.

Worked cut. The parent says: an MCP server exposes seven tools and calls the core. A caller can
ask each tool on its own, and each tool has its own question and its own right answer. One pull
request cannot carry seven sets of checks. The parent is not implemented.

1. The list is seven lines, one tool each. "Implement the core", "stand up MCP", and "the public endpoint" are not lines.
2. If those tools depend on a result shape that no accepted RFC and no merged issue has settled, that shape is one RFC issue. The tool stories wait until it is merged with `Status: accepted`.
3. A date whose answer comes from a different official notice is a `data` story of its own. A tool story names the pinned `holidays` version, or names the gap. It does not also correct another country's dates.
4. Two tools stay apart, because a caller can take one and leave the other, and their checks differ.
5. The first story reads: for `CN` on `2025-10-11`, the caller receives that day's type. Left out: the other six tools, HTTP, and the site. Source: the pinned `holidays` version, plus either the notice link or the words "not yet checked against the State Council notice". The check is that one question and its right answer. The story includes the core code that this one answer needs.
6. The other six tools are six stories, each depending on the first. The parent lists the seven in that order.
7. The agent opens the seven sub-issues and writes the four statements. The owner does not open them one by one. Implementation of a child starts after `Staring531` comments a line `Adopted` on it.

The owner changes a cut by commenting on the parent. The agent rewrites the sub-issues to match
that comment. It does not start a child that has no `Adopted` line.

## Project statuses

The project belongs to the user `Staring531`, number 1, title `Calendo_Service_Devolpment`, at
https://github.com/users/Staring531/projects/1 . The project is private. On 2026-11-06 the Status
field had these five options, in this order.

| Status | When this repository's workflow writes it | Why |
| --- | --- | --- |
| `Backlog` | It does not | The column remains. Where a new card lands is chosen by a built-in project workflow below. The API does not return that target value |
| `Designing` | A `pull_request` event of type opened, synchronize, or reopened. A changed file is `rfcs/CRFC-NNNN-slug.md` or the matching `.zh.md`, and the body names at least one issue | The RFC is still being drafted. Implementation has not started |
| `Ready` | An `issue_comment` event of type created. The comment author's login is `Staring531`, and one line of the comment is `Adopted` | The owner has adopted the issue. Work can start |
| `Verifying` | The same pull request event names an issue, and the changed files do not match the RFC condition above | The implementation pull request names the issue and is waiting for checks and approval |
| `Done` | An `issues` event of type closed | The issue is closed |

The RFC condition is decided before `Verifying`. A pull request that both edits an RFC file and
contains `Closes` moves the card to `Designing`.

Two kinds of text in the body move a card: `Closes`, `Fixes`, or `Resolves` with a number or a
full issue URL, and any URL of an issue in this repository. `records` accepts only the first kind,
and it accepts exactly one issue.

When `PROJECT_TOKEN` is unset, `.github/workflows/project-status.yml` prints a warning and exits 0.
It is not a check the ruleset requires, so the pull request does not turn red. The Actions secrets
list read on 2026-11-06 was empty, so this workflow was not moving cards.

The script looks up the Status option by name. Option ids are not written into the code. After a
rename, a move to the old name fails and the log contains `project status <name> does not exist`.

## Built-in project workflows

The switches below were read from the project API on 2026-11-06. The API returns the name and
whether the workflow is enabled. It does not return the Status value each workflow writes. That
value is in the project's Workflows menu, opened from the top right of the board.

| Name | Enabled | What it responds to |
| --- | --- | --- |
| Auto-add to project | yes | Adds an issue or pull request opened in the repository when it matches the filter |
| Auto-add sub-issues to project | yes | Adds a sub-issue when it is opened |
| Item added to project | yes | Sets Status to the value chosen in the menu when a card enters the project |
| Item closed | yes | Sets Status to the value chosen in the menu when an issue or pull request is closed |
| Pull request linked to issue | yes | Sets the linked issue's Status to the value chosen in the menu |
| Auto-close issue | yes | Closes the issue when its Status becomes the value chosen in the menu. GitHub's description of this workflow is that trigger |
| Pull request merged | no | Would set Status when a pull request is merged. It is off, so a merge does not move a card through this workflow |

With Pull request merged off, a card reaches `Done` because the issue closes. A `Closes` line
makes GitHub close the issue on merge. The `issues: closed` event then runs this repository's
workflow and writes `Done`. Item closed runs as well, so both can write Status.

## GitHub Actions workflows

The three files are under `.github/workflows/`.

### CI

File `ci.yml`. The workflow name is `CI`.

It runs on:

- a push to `main`
- a pull request targeting `main`, for opened, synchronize, reopened, labeled, and unlabeled
- a manual `workflow_dispatch`
- a `workflow_call` from the Release workflow, with the tag or commit to validate

`labeled` and `unlabeled` are included so that adding or removing `skip-changelog` runs `records`
again.

The permission is `contents: read`. A new run for the same ref cancels the run still in progress.

| Job | What it does |
| --- | --- |
| `style` | `ruff format --check`, `ruff check`, actionlint, and the shape of every changelog entry and RFC |
| `typecheck` | pyright in strict mode over `src/`, `scripts/`, and `tests/` |
| `test (Python 3.12)` and `test (Python 3.14)` | pytest with branch coverage and sockets disabled. The 3.14 job stores `coverage.xml` as an artifact for 7 days. There is no coverage threshold |
| `package` | `uv build`. The wheel contains `calendo/py.typed` and `LICENSE`. Installed into an empty environment, it reports the version in `pyproject.toml` |
| `records` | The next table. On any other event the job prints one line and succeeds without checking |
| `ci` | `needs` every job above. `if: always()`, so a cancelled or skipped job is part of the result. Any result other than `success` fails the job |

The ruleset requires the check named `ci`. When another job fails, `ci` fails, and the merge stays
blocked.

The three `records` steps on a pull request:

| Step | Skipped when | What it checks |
| --- | --- | --- |
| A changelog entry ships with the change | the label `skip-changelog` | The branch adds a changelog pair relative to `main` |
| Revised RFCs raise their version | neither label skips it | An RFC that changed after landing raised its version |
| The pull request closes one adopted leaf issue | `skip-changelog` or `dependencies` | Exactly one adopted issue, with no open sub-issue |

### Project status

File `project-status.yml`. The workflow name is `Project status`.

It runs on:

- `pull_request` opened, synchronize, and reopened. It does not run on closed, and it does not run
  on the merge itself
- `issue_comment` created
- `issues` closed

Permissions are `contents: read`, `pull-requests: read`, and `issues: read`. The step that moves
the card reads the secret `PROJECT_TOKEN`. It does not use `github.token` for that call, and it
does not use the App token.

On a pull request, the workflow lists changed paths with `github.token`, then runs
`scripts/project_status.py`. The status choice is the project table above. The script finds user
`Staring531`'s project number 1, then the Status option by name. An issue that is not on the
project is added, and the field is then set.

This workflow is not part of `ci`. A missing secret warns and exits 0.

### Release

File `release.yml`. The workflow name is `Release`.

It runs on a pushed tag matching `v*`, or on a manual run that names an existing tag.

| Job | What it does |
| --- | --- |
| `preflight` | Runs `scripts/check_release.py` on the tag's tree. When that tag already has a GitHub Release, the later jobs do not run |
| `validate` | Calls the CI workflow on that tag |
| `release` | Asks for `contents: write`. Runs `uv build`, writes `SHA256SUMS`, uses `changelog/<version>/RELEASE.md` as the Release body, and uploads `dist/*` |

A pushed tag is never moved. Cutting a release is the owner's call. This workflow is not a check
the ruleset requires.

## PROJECT_TOKEN

`PROJECT_TOKEN` is a classic personal access token stored as an Actions secret of that name.
Project status uses it to edit cards on the user project.

The repository `GITHUB_TOKEN` is limited to this repository and cannot edit a user project. The
App is not granted the Projects permission. On a fine-grained token, Projects appears under
Organization permissions. When the resource owner is a user account, Account permissions has no
Projects entry. GitHub's documentation lists access to Projects owned by a user account as a
fine-grained token gap.

The token is a classic token with only the `project` scope (Full control of projects). The
repository is public, so `repo` stays unchecked. The token can edit every project on the account.
GitHub does not limit a classic `project` token to one board. The generation page is
https://github.com/settings/tokens/new .

Paste the token only after `Paste your secret:`. Leave it out of the command. From the checkout:

```sh
env -u GH_TOKEN gh secret set PROJECT_TOKEN --repo Staring531/calendo_service
```

`env -u GH_TOKEN` drops the App token that `.envrc` set. Calling `actions/secrets/public-key`
with that token returns 403 and the body `Resource not accessible by integration`. After it is
unset, `gh` uses the keyring login `Staring531`, which can write the secret.

A token that has appeared in a command line or in chat is exposed. Revoke it at
https://github.com/settings/tokens and generate another.

## What this read returned, and what the API left out

Read on 2026-11-06: the repository is public; squash is the only merge method; the `project-main`
parameters are the table above; the Actions secrets list was empty; the five statuses are the
table above; the seven project workflow switches are the table above.

The API did not return the Status value each built-in project workflow writes. It also did not
return the permission list or the repository selection of the App `cursor-cf`. The merged pull
request [#12](https://github.com/Staring531/calendo_service/pull/12), authored by `app/cursor-cf`,
shows that the App can open a pull request. The permission list is checked on the App's settings
page: Contents, Pull requests, and Issues at read and write, Metadata at read. Administration,
Projects, Actions, and Secrets stay off. The installation selects this repository only.
