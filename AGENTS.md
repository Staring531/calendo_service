# AGENTS.md

Calendo answers holiday and working-day questions for AI agents. One Python core is the only source
of answers; an MCP server and a read-only HTTP API adapt it, and the site calls the HTTP API.

Read [`.agents/skills/calendo-dev/SKILL.md`](.agents/skills/calendo-dev/SKILL.md) before your first
edit. It holds the conventions, the verification table and the record-and-ship contract, and
points to a reference for each kind of task. The product background is
[`docs/product/calendo-mvp.zh.md`](docs/product/calendo-mvp.zh.md).

The rules that hold for every change:

1. **Requirements come from the product background, an issue or the owner.** Write down what you
   will build as questions with their answers and each answer's source, and wait for the owner's
   yes before you change behaviour they have not approved.
2. **The service makes no network call at run time**, and no test reaches the network.
3. **No date fact is typed into code or produced by a model.** It comes from the pinned
   `holidays` version or a committed fixture that links its official source.
4. **When the library, a fixture and an expected answer disagree, stop** and list the dates with
   all three values. Which source wins is the owner's call.
5. **Open design decisions go through an RFC** in `rfcs/`, in a pull request of their own, before
   the code that depends on them.
6. **Every change ships a changelog entry pair** in `changelog/unreleased/`, English and Chinese.
7. **Branch and pull request against `main`, squash-merged.** Never push to `main`; never force-push
   without the owner's yes.
8. **Report what you ran and what it printed.** `sh scripts/check.sh` is the full chain CI runs.
   What you did not run, say you did not run.
