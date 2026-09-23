#!/usr/bin/env python3
"""
check_pr_bundle.py

用途：核验"测试、生产代码、changelog 在同一个 PR 里产出"这条规则——依据是
Google工程实践指南原文"tests should be added in the same PR as the production
code unless the PR is handling an emergency"，以及changelog同PR惯例（多个独立
来源：go-changelog工具设计前提、linebender/druid PR#889、lando/lando issue#3710、
CodeForFire/lagebuch PR#434）。

**本脚本不含任何项目专属内容**，套用前需要在 --src-paths-file 里配置本项目的
生产代码路径。

唯一认可的例外是 emergency——这不是本脚本发明的口子，是 Google 原文明确给出
的例外场景（"unless the PR is handling an emergency"），emergency 的定义 Google
也给了：修复严重影响生产环境用户的bug、堵一个重大安全漏洞、处理紧急法律问题
这类，不包括"想这周而不是下周发布""开发者催着要合"这种软性deadline。

用法：
    python scripts/check_pr_bundle.py --base origin/main --head HEAD \\
        --src-paths-file path/to/src_paths.txt \\
        --test-path-prefix tests/ \\
        --changelog-path-prefix changelog/ \\
        --pr-body-file <path>
"""

import argparse
import re
import subprocess
import sys

EMERGENCY_MARKER = re.compile(r"emergency:\s*(.+)", re.IGNORECASE)


def load_paths(path: str) -> list[str]:
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]


def get_changed_files(base: str, head: str) -> list[str]:
    result = subprocess.run(
        ["git", "-c", "core.quotepath=false", "diff", "--name-only", f"{base}...{head}"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def touches_any(changed_files: list[str], prefixes: list[str]) -> bool:
    return any(f.startswith(p) for f in changed_files for p in prefixes)


def get_emergency_reason(pr_body: str) -> str | None:
    m = EMERGENCY_MARKER.search(pr_body)
    return m.group(1).strip() if m else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--src-paths-file", required=True)
    parser.add_argument("--test-path-prefix", default="tests/")
    parser.add_argument("--changelog-path-prefix", default="changelog/")
    parser.add_argument("--pr-body-file")
    args = parser.parse_args()

    changed_files = get_changed_files(args.base, args.head)
    src_paths = load_paths(args.src_paths_file)

    if not touches_any(changed_files, src_paths):
        print("未改动生产代码路径，跳过 test/changelog 同 PR 检查。")
        return 0

    pr_body = ""
    if args.pr_body_file:
        try:
            with open(args.pr_body_file, encoding="utf-8") as f:
                pr_body = f.read()
        except FileNotFoundError:
            pass

    emergency_reason = get_emergency_reason(pr_body)
    if emergency_reason:
        print(
            f"标记为 emergency，理由：{emergency_reason}\n"
            "放行，但按 Google 工程实践指南的要求，emergency 解决后应该回头做一次"
            "完整补充 review（本脚本不能替你做这一步，只能提醒）。"
        )
        return 0

    missing = []
    if not touches_any(changed_files, [args.test_path_prefix]):
        missing.append(f"测试改动（{args.test_path_prefix} 下没有文件变化）")
    if not touches_any(changed_files, [args.changelog_path_prefix]):
        missing.append(f"changelog 条目（{args.changelog_path_prefix} 下没有文件变化）")

    if missing:
        print(
            "本次改动触碰了生产代码，但缺少以下同 PR 应该一起出现的东西：",
            file=sys.stderr,
        )
        for m in missing:
            print(f"  - {m}", file=sys.stderr)
        print(
            "\n如果这确实是 Google 定义的 emergency（严重生产bug/安全漏洞/紧急法律问题，"
            "不包括赶软性deadline），在 PR 描述里写一行 'emergency: <理由>' 再重新触发。",
            file=sys.stderr,
        )
        return 1

    print("生产代码、测试、changelog 都在同一个 PR 里，通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
