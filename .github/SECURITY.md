# Security Policy

[中文版](SECURITY.zh.md)

## Supported versions

Calendo has not been released yet. From the first release on, it ships from `main` with no
maintenance branches: a fix lands in the next release, and only the most recent release is
supported.

## Reporting a vulnerability

Report privately, through GitHub's
["Report a vulnerability"](https://github.com/Staring531/calendo_service/security/advisories/new)
form. It opens a draft advisory only the maintainer can see, and keeps the report, the fix and the
disclosure together. Do not open a public issue or pull request for a security problem.

A report is most useful with the affected version or commit, where it ran (the public endpoint,
the site, or a local run), and the smallest request that reproduces it. Expect an acknowledgement
within days, then an assessment of what it affects.

## What counts

Calendo is a read-only service that answers date questions without authentication. Within that
design, these are in scope:

- A request that makes the service reach the network, read a file outside its own data, or run
  anything it was not built to run.
- A single request whose cost is far out of proportion to its answer, such as one that pins a
  worker or grows memory without bound.
- Input that reaches an MCP client or the site as something other than data: markup or
  instructions smuggled through a parameter and echoed back.
- A release asset that does not match the tag's source or the `SHA256SUMS` published with it, and
  credentials exposed in the repository, its CI logs or its releases.

These are not security problems:

- A date Calendo gets wrong. That is a data defect; report it with the
  [data form](https://github.com/Staring531/calendo_service/issues/new?template=data.yml).
- Request volume against the public endpoint. Report a request that is expensive on its own, not
  a flood of cheap ones.
- Vulnerabilities in a dependency, such as `holidays`, that are not reachable through Calendo.
  Report those to the dependency's maintainers.
