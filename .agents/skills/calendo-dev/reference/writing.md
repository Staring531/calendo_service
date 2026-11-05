# Writing what a reader sees

Loaded on demand from `SKILL.md`. It applies to the README, `docs/`, changelog prose, RFCs, PR
bodies, error messages, and the MCP tool descriptions a model reads to decide which tool to call.

## Every language

- **Specific beats general.** Name the tool, the field, the error code, the date, the number.
  "2025-09-29 to 2025-10-12 returns 5" beats "ranges are handled correctly".
- **Lead with what happened or what to do.** The first sentence of a section, an error or a tool
  description carries the point; the detail follows.
- **Short paragraphs, one idea each.** Prefer a sentence over a clause pile.
- **Subtract first.** Remove the sentence that only announces the next one, the caveat nobody
  needs, the summary of what was just said.
- **State uncertainty as uncertainty.** "Not yet checked against the State Council notice" is a
  fact a reader can act on; do not soften it, do not hide it.
- **No decoration.** No emoji, no exclamation marks, no bolded keywords scattered through a
  paragraph, no marketing words: powerful, seamless, robust, revolutionary, "we are excited".
- **Never "it's not X — it's Y".** Say what it is.

## Tool descriptions and errors

A model reads these, not a person, and acts on every word:

- A tool description says when to use the tool, the argument formats (ISO dates `YYYY-MM-DD`,
  ISO 3166-1 alpha-2 country codes), whether ranges include both ends, and what each returned
  field means. A behaviour that surprises (the same result for `days=0` and `days=1` from a
  non-working day) is stated outright.
- An error says what was wrong and how to fix the request, in one or two sentences a model can
  repeat to its user: "2031 is outside the supported years 2025–2027. Ask about a year in that
  range."
- A word added to a tool description is paid for on every request of every conversation that
  loads it. Keep each one as short as its job allows.

## Chinese

The voice: an engineer writing for developers, plain and direct.

- 中英文、数字之间留一个半角空格；标点用全角；括号内全为英文或数字时用半角括号。
- 技术名词保持英文原样：Agent、MCP、HTTP API、CLI、Token、pull request、commit、tag、workflow。界面与字段名照抄原文，用反引号或「」引出。
- 段落短，一段一件事；先写主语和动作，再写条件与原因。
- 禁用：翻案句（不是……而是……、并非……而是……、与其说……不如说……）；路标词（值得注意的是、说白了、换句话说、不难发现、先说结论）；名词化（进行了、实现了对……的、起到了……作用）；黑话（赋能、抓手、闭环、底层逻辑、全链路、生态、沉淀、颗粒度、无缝、强大）。
- 不用破折号「——」连接句子，不用感叹号，不自行加粗。
- 翻译腔要改：「对于……而言」开头、每句一个「当……时」、「的」连用超过两个、「被」字句堆叠。

## English

The register of VS Code's release notes: a developer writing for developers, plain and unhyped.
Concrete nouns and numbers carry the weight; adjectives do not. No rhetorical questions, no
second-person cheerleading.

## Before you call it done

Read it once as the reader: a developer deciding whether to integrate, a model deciding which tool
to call, a user wondering whether to trust a date. Cut what that reader would skip. Check every
date, number and name against its source.
