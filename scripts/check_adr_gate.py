#!/usr/bin/env python3
"""
check_adr_gate.py

用途：在 PR 里检查——如果改动触碰了"架构敏感路径"，但这个 PR 里没有新增/修改
docs/decisions/ 下的 ADR 文件，也没有在 PR 描述里显式写明不需要 ADR 的理由，
就让 CI 失败，逼着改动的人停下来判断一次，而不是直接合并。

**重要限制，必须先说清楚，不是本脚本能力范围**：
判断一个改动是不是"架构级"，本质是人的判断，不是脚本能语法层面验证的东西——
这一点在 ADR 相关的多个独立来源里都被明确指出：AI/脚本不能替你决定什么算
architecturally significant，只能降低把好的判断写下来的成本，不能生成判断本身。
所以这个脚本做的事，严格来说只是一个"路径命中就提醒"的启发式，命中不代表
真的需要 ADR，没命中也不代表真的不需要——它只是防止"改了敏感路径但完全没人
想到该不该写 ADR"这种最低级的遗漏，不能替代人工判断。

**本脚本不含任何项目专属内容，是通用工具，套用到任何项目前必须先做两件事**：
1. 在 `--sensitive-paths-file` 指定的文件里，逐行列出你自己项目的架构敏感路径
   （数据源、协议边界、核心状态机之类——具体是什么，只有你的项目自己知道，
   这个列表不该由本脚本替你猜）。
2. 确认你的项目用的是 PR-based 工作流（改动先开 PR，CI 在 PR 上跑）。如果是
   直接 push 到 main、没有 PR 这一步，本脚本要改成 pre-commit/pre-push hook
   才能起作用，CI-on-PR 这个触发方式就不成立。

用法（假设 PR 场景）：
    python scripts/check_adr_gate.py --base origin/main --head HEAD \\
        --sensitive-paths-file path/to/sensitive_paths.txt --pr-body-file <path>
"""

import argparse
import re
import subprocess
import sys

NO_ADR_NEEDED_MARKER = re.compile(r"no-adr-needed:\s*(.+)", re.IGNORECASE)


def load_sensitive_paths(path: str) -> list[str]:
    """
    从外部文件加载"架构敏感路径"列表，每行一个路径前缀，`#` 开头的行当注释跳过。
    这个列表刻意不写死在脚本里——它是纯粹的项目专属信息，哪些路径算敏感、
    对应哪条 ADR，只有具体项目的维护者知道，脚本不该替任何项目做这个判断。
    """
    with open(path, encoding="utf-8") as f:
        return [
            line.strip()
            for line in f
            if line.strip() and not line.strip().startswith("#")
        ]


def get_changed_files(base: str, head: str) -> list[str]:
    # -c core.quotepath=false：避免 git 对包含非 ASCII 字符（比如中文路径）的
    # 文件名做八进制转义，否则下面的路径前缀匹配会失效——这个问题是实测发现的，
    # 不是理论推测：用中文占位路径测试时，git diff --name-only 默认输出的是
    # 转义后的八进制字符串，跟 SENSITIVE_PATHS 里的原始字符串完全匹配不上。
    result = subprocess.run(
        ["git", "-c", "core.quotepath=false", "diff", "--name-only", f"{base}...{head}"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def touches_sensitive_path(changed_files: list[str], sensitive_paths: list[str]) -> list[str]:
    hits = []
    for f in changed_files:
        for sensitive in sensitive_paths:
            if f.startswith(sensitive):
                hits.append(f)
    return hits


def has_new_adr(changed_files: list[str]) -> bool:
    # 命名规则：docs/decisions/YYYY-MM-DD-NNNN-short-title.md（英文，默认版本），
    # 或 docs/decisions/YYYY-MM-DD-NNNN-short-title.zh.md（中文版本）。
    # 排除 README.md 和 ADR-TEMPLATE.md/.zh.md——它们在 docs/decisions/ 下但不是 ADR 本身。
    return any(
        f.startswith("docs/decisions/")
        and re.match(
            r"docs/decisions/\d{4}-\d{2}-\d{2}-\d{4}-.+(?:\.zh)?\.md$", f
        )
        for f in changed_files
    )


def has_no_adr_needed_marker(pr_body: str) -> str | None:
    m = NO_ADR_NEEDED_MARKER.search(pr_body)
    return m.group(1).strip() if m else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="对比基准分支，比如 origin/main")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument(
        "--sensitive-paths-file",
        required=True,
        help="逐行列出架构敏感路径前缀的文件，项目专属，脚本本身不内置任何路径",
    )
    parser.add_argument(
        "--pr-body-file",
        help="PR 描述文本文件路径，用于检查是否有 no-adr-needed: <理由> 标记",
    )
    args = parser.parse_args()

    changed_files = get_changed_files(args.base, args.head)
    sensitive_paths = load_sensitive_paths(args.sensitive_paths_file)
    sensitive_hits = touches_sensitive_path(changed_files, sensitive_paths)

    if not sensitive_hits:
        print("未触碰架构敏感路径，跳过 ADR 检查。")
        return 0

    if has_new_adr(changed_files):
        print("检测到本次改动包含新增/修改的 ADR 文件，通过。")
        return 0

    pr_body = ""
    if args.pr_body_file:
        try:
            with open(args.pr_body_file, encoding="utf-8") as f:
                pr_body = f.read()
        except FileNotFoundError:
            pr_body = ""

    reason = has_no_adr_needed_marker(pr_body)
    if reason:
        print(f"未新增 ADR，但 PR 描述中显式说明了理由：{reason}")
        print("放行，但这条理由会留在 PR 记录里，可追溯。")
        return 0

    print(
        "本次改动触碰了以下架构敏感路径，但既没有新增 ADR，"
        "PR 描述里也没有写 'no-adr-needed: <理由>'：",
        file=sys.stderr,
    )
    for f in sensitive_hits:
        print(f"  - {f}", file=sys.stderr)
    print(
        "\n提醒：命中敏感路径不代表这次改动一定需要 ADR，这只是一个启发式检查，"
        "是否真的需要 ADR 仍然要你自己判断（参考 docs/decisions/README.md 的标准）。"
        "如果判断不需要，请在 PR 描述里加一行 'no-adr-needed: <理由>' 再重新触发 CI。",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
