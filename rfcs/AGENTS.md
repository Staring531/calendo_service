# AGENTS.md

The root [AGENTS.md](../AGENTS.md) applies here too. On a conflict, this file wins for `rfcs/`.
[`README.md`](README.md) is the process and the index. Copy [`TEMPLATE.md`](TEMPLATE.md) and
[`TEMPLATE.zh.md`](TEMPLATE.zh.md).

## Drafting

- One decision per pair: `CRFC-NNNN-<slug>.md` and `.zh.md`. Take the next number after the last
  index row, and add the row in the same pull request.
- Open an RFC when a change needs a choice later work builds on: the shape of an answer, a data
  source, a framework, the deployment, how a wrong date gets corrected. The open questions in
  `docs/product/` are where the first ones come from. An agent may draft an RFC. Accepting it is
  the owner's call, and an agent never sets `Status: accepted`.
- The RFC and the implementation it decides are different pull requests. The implementation cites
  the RFC by number.
- `Status: draft` does not authorise implementation, including a draft that has already merged.
  `Status` is otherwise `accepted`, `implemented`, `superseded` or `rejected`. A superseded RFC
  names its successor in its first paragraph.
- A landed RFC changes rarely. When it must, raise the version and list the items under
  `## Changes` (`### v1.1.0`, then Added / Removed / Updated), in both languages. `## Changes`
  keeps its English heading on both sides.

`scripts/check_rfcs.py` checks the shape. On a pull request it checks that a revised RFC raised
its version.
