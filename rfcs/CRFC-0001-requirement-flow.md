# CRFC-0001 From direction to workable issue

- Status: draft
- Start Date: 2026-11-05
- RFC PR: [#9](https://github.com/Staring531/calendo_service/pull/9)
- Implementation PR: [#N](https://github.com/Staring531/calendo_service/pull/N)

[中文版](CRFC-0001-requirement-flow.zh.md)

## Summary

Work reaches code through four levels: direction, requirement, decision, implementation. Only an
issue whose clarification record the owner has approved authorises behaviour. A product document
gives direction and never authorises work on its own. A request larger than one workable unit
becomes a parent issue and is split before anything in it is approved. An RFC is written only when
an approved clarification names the decision it settles. Each status on the GitHub Project board
has an entry condition tied to one of these artifacts, and the person who may move a card is named.
`AGENTS.md` becomes the entry point that says where each level lives.

## Motivation

Issue [#8](https://github.com/Staring531/calendo_service/issues/8) asked for the whole MCP server:
seven tools, a public endpoint and a ten-question acceptance run. The core it calls is an empty
`src/calendo/__init__.py`. Within one comment the issue was treated as approved, because every line
of it was copied from `docs/product/calendo-mvp.zh.md`, and the card was moved straight to
Designing, because the product document says the MCP SDK choice "goes through an RFC". No scope was
agreed, nothing was split, and none of the open boundary questions reached the owner.

The repository's rules allowed each step:

- `AGENTS.md` rule 1 and the dev skill list the product background, an issue and the owner's words
  as equal sources of requirements. A line in a coarse document therefore counts as approved.
- Nothing says how small a piece of work must be before it can be approved.
- "Write it down as questions and wait for a yes" has no fixed shape and no signal that marks the
  yes, so a single comment can stand in for it.
- The dev skill calls the product document's open questions "the queue" of RFCs, so an agent works
  through them on its own.
- The Project's statuses (Clarifying, Investigating, Designing, Ready, Accepted) appear nowhere in
  the repository, and `gh project item-edit` changes a card without checking anything.
- `AGENTS.md` names one document as "the product background" and gives three lines of overview, so
  an agent learns nothing about how mature that document is or what the repository holds.

Fixing #8 alone would leave all six in place for the next large request.

## Guide-level explanation

Take a request as large as "build the HTTP API".

1. Someone opens an issue. The board puts it in Backlog.
2. The agent checks its size against the workable-unit test. It fails: seven endpoints, a framework
   not chosen, a core that does not exist. The agent writes a clarification record that says so,
   marks the issue as a parent, and proposes children: the core functions the first endpoints
   need, then `GET /v1/days/{date}`, then the rest. The card moves to Clarifying.
3. The owner reads the record, changes the split and approves it. The parent never moves to Ready;
   it tracks its children.
4. Each child gets its own clarification record: what a caller sends, what comes back, where each
   date fact comes from, and what is out of scope. One child needs evidence first, for example what
   `holidays` 0.108 returns for 2027 in CN. That child moves to Investigating until the evidence is
   written into it.
5. One record lists "HTTP framework" under decisions needed, and the owner agrees it must be settled
   now. Only then does an RFC pull request open, citing that issue. The card moves to Designing.
6. The owner merges the RFC with `Status: accepted` and approves the child. The child moves to
   Ready. Implementation starts.

The product document is read at step 2 to propose the split. It does not skip steps 3 to 6.

## Reference-level explanation

### Levels

| Level | Where it lives | What it may do | What it may not do |
| --- | --- | --- | --- |
| Direction | Documents under `docs/product/` | State what is being built and why | Authorise any work |
| Requirement | An issue with an approved clarification record | Authorise one card's behaviour and scope | Make a design choice |
| Decision | An RFC under `rfcs/` with `Status: accepted` | Settle one choice later work depends on | Widen a requirement's scope |
| Implementation | A pull request that cites an approved issue | Deliver that issue | Go beyond the clarification record |

When the owner's later words conflict with a document, the owner's words win and the record says
which line they override. That rule is unchanged.

### Workable unit

An issue is a workable unit when all four hold:

1. It delivers one set of behaviours a caller can observe, such as two MCP tools, not one product.
2. One implementation pull request can deliver it.
3. Every date fact in its answers has a source, or is listed as a gap.
4. What it depends on exists, or is another issue.

An issue that fails is a parent issue. It holds scope and the split, uses GitHub sub-issues for its
children, never moves to Ready, and closes when its children are done.

### Clarification record

A comment on the issue with these headings, in this order:

1. In scope: the behaviours this issue delivers.
2. Out of scope: what it does not do, and which issue holds each item.
3. Questions and answers: the request, the response, and the source of every date fact (an
   official notice with its link, an observation of `holidays` at its pinned version, or a gap).
4. Assumptions: each thing the agent inferred, one per line, for the owner to confirm or reject.
5. Split: the proposed children, when the issue fails the workable-unit test.
6. Decisions needed: each choice that needs an RFC, and why it must be made now.

An agent edits the record when the owner asks for changes; it does not approve its own record.

### RFC entry

An RFC is written when an approved clarification record names it under decisions needed and the
owner agrees it is due now. The RFC's Motivation cites that issue. The open questions in a product
document are candidates. Each becomes an issue, and the document links to those issues instead of
keeping the list. Process decisions such as this one enter the same way, from the owner's request.

### Board statuses

The `Accepted` status is removed. A pull request that delivers an issue says `Closes <issue URL>`;
merging it closes the issue, and the Project's "Item closed" workflow moves the card to Done.

| Status | Entry condition | Who moves it |
| --- | --- | --- |
| Backlog | The issue is added | The Project workflow |
| Clarifying | A clarification record is posted | Agent |
| Investigating | The record lists a gap and the issue states the evidence that would close it | Agent |
| Designing | A draft RFC pull request is open, named in an approved record | Agent |
| Ready | The record is approved, the issue is a workable unit, and its dependencies are in place | Owner |
| In Progress | A branch for the issue exists | Agent |
| Verifying | A pull request is open with the output of `sh scripts/check.sh` in its body | Agent |
| Blocked | A comment names what it waits on: an owner's call, an upstream release, an official notice | Agent or owner |
| Done | The issue closed | The Project workflow |
| Rejected | The owner declined it | Owner |

Each time an agent moves a card it comments on the issue: the entry condition met and a link to the
artifact that meets it. An agent never moves a card into Ready or Rejected.

### Mechanical check

The `records` job in CI checks that a pull request cites an issue carrying the approval signal,
unless the pull request is labelled as one that delivers no behaviour (documentation, tooling, an
RFC). Which signal it reads is open below.

### What the implementation changes

- `AGENTS.md`: a project overview, the current state of the repository, where each level lives,
  how work flows (a paragraph and a link to the status table), and the existing rules with rules 1
  and 5 rewritten to match this RFC. It names `docs/product/` as the directory of direction
  documents instead of one file.
- The dev skill: the levels, the workable-unit test, the clarification record and the RFC entry
  rule replace "Before any code" and the sentence that calls the open questions a queue.
- `.github/CONTRIBUTING.md` and its Chinese counterpart: the status table.
- Issue forms: in-scope and out-of-scope fields, and a note that a large request becomes a parent.
- The pull request template: `Closes <issue URL>`, kept.
- `scripts/check_changelog.py` or a new script, and `ci.yml`: the mechanical check.
- `docs/product/calendo-mvp.zh.md`: a line under the title saying it is a direction document, and
  the open-questions list replaced with links to issues.
- Repository labels: the approval signal if it is a label, `type:bug`, `type:data`,
  `type:feature`, `type:investigation` (the issue forms already apply them) and `skip-changelog`
  (CI already reads it).
- Project 1: remove `Accepted`, turn on "Item closed", set "Pull request linked to issue" to move
  the card to Verifying.

## Drawbacks

A small, obvious change now passes through a clarification record and an approval. The record can
be three lines, but the wait for the owner remains.

The board and the repository still are not one system. The status table and the comment on each
move rely on the agent following them; only the approval signal is checked by a machine.

## Rationale and alternatives

Fixing #8 alone, by splitting it by hand, leaves every rule that let it happen. The next large
request repeats it.

Treating the product document as a specification, and refining it until it is fine enough, puts
scope decisions in a file that has no approval step and no link to the work. Issues already have
both.

Making the board enforce the flow is not possible with Project workflows: they set a status on an
event and check nothing. The check belongs in CI, which already gates every pull request.

Keeping `Accepted` as a manual acceptance step was considered. The owner chose that merging
delivers the issue, so the pull request template's `Closes` stays and the extra status goes.

Doing nothing leaves an agent free to read any line of a direction document as approved work.

## Unresolved questions

- The approval signal. The options: the owner adds an `approved` label to the issue, which CI can
  read; the owner replies with a fixed phrase, which CI can read only by parsing comments; the
  owner moves the card to Ready, which CI cannot read without a Project token. The mechanical check
  waits on this answer.
- Who sets an RFC to `implemented` after its implementation merges. This RFC does not decide it.
- Whether parent issues get their own label in addition to GitHub's sub-issue link.

---

## Changes

### v1.0.0

- Initial version
