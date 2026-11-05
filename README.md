# Calendo

[中文版](README.zh.md)

Holiday and working-day answers for AI agents, with every date's source stated.

Calendo answers the date questions a model should not guess: is 2025-10-11 a working day in China,
what is the third working day after 2025-09-26, how many working days fall between 2025-09-29 and
2025-10-12, which long breaks does 2026 have. Each answer carries the day's type (statutory
holiday, shifted rest day, adjusted workday, weekend or workday), how well its data is verified,
and the version of the data it came from.

## Status

Calendo has not been released, and no answers are implemented yet. This repository holds the
engineering baseline (checks, CI, the release workflow, the changelog and RFC formats) and the
[product background](docs/product/calendo-mvp.zh.md) the MVP is built from.

The MVP is planned as three layers over one Python core:

| Layer | For | Planned |
| --- | --- | --- |
| MCP server | AI agents in Claude, Cursor and other MCP clients | A public remote endpoint with 7 read-only tools |
| HTTP API | Developers and the site | 7 read-only endpoints under `/v1` |
| calendo.day | Developers deciding whether to integrate | One page: connect a client, try a date, read how the data is checked |

China comes first, checked day by day against the State Council's holiday notices. Other countries
answer through the same tools from the [holidays](https://github.com/vacanza/holidays) library and
are marked unverified until they are checked. The service makes no network call to answer.

## Development

```sh
uv sync
sh scripts/check.sh
```

[CONTRIBUTING](.github/CONTRIBUTING.md) covers the setup, the checks, the working rules and how a
change ships. Coding agents start at [AGENTS.md](AGENTS.md).

| Read | For |
| --- | --- |
| [Product background](docs/product/calendo-mvp.zh.md) | What the MVP is, and the questions still open |
| [Design RFCs](rfcs/README.md) | Decisions later work builds on |
| [Changelog](CHANGELOG.md) | What shipped, release by release |
| [Security policy](.github/SECURITY.md) | How to report a vulnerability |

## License

[MIT](LICENSE)
