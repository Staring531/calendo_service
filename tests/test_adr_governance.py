"""
tests/test_adr_governance.py

用途：把 docs/decisions/README.md 里写的规则，转成可以自动跑的测试，而不是
只靠人读一遍 README 来保证遵守。README 改了规则，这里的测试也要跟着改，
两者要保持同步——这是本测试套件本身的维护前提，不是自动的。

覆盖的规则，逐条对应 README 里的章节：
  - 文件命名：YYYY-MM-DD-NNNN-标题.md + 对应的 .zh.md
  - 编号：四位数字，从 0001 开始连续递增，不跳号、不重复
  - Status 字段：只能是 Proposed / Accepted / Deprecated / Superseded by ADR-XXXX 之一
  - 必需章节：Status / Context / Decision / Consequences 都要存在
  - 每份英文 ADR 必须有对应的中文版，反之亦然
  - AGENTS.md 里指向 ADR 的链接必须指向真实存在的文件（防止改名后链接失效）

运行：pytest tests/test_adr_governance.py -v
"""

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
DECISIONS_DIR = REPO_ROOT / "docs" / "decisions"
AGENTS_MD = REPO_ROOT / "AGENTS.md"

# 对应 README「文件命名与目录结构」一节的正则
ADR_FILENAME_RE = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2})-(?P<num>\d{4})-(?P<slug>[a-z0-9-]+)(?:\.(?P<lang>zh))?\.md$"
)

VALID_STATUS_PREFIXES = ("Proposed", "Accepted", "Deprecated", "Superseded by ADR-")

REQUIRED_SECTIONS = ["Status", "Context", "Decision", "Consequences"]


def _adr_files() -> list[Path]:
    if not DECISIONS_DIR.exists():
        return []
    return sorted(
        p
        for p in DECISIONS_DIR.glob("*.md")
        if ADR_FILENAME_RE.match(p.name) and not p.name.startswith("TEMPLATE")
    )


def test_decisions_dir_exists():
    assert DECISIONS_DIR.exists(), "docs/decisions/ 目录不存在"


def test_template_files_exist():
    assert (DECISIONS_DIR / "ADR-TEMPLATE.md").exists(), "缺少 ADR-TEMPLATE.md"
    assert (DECISIONS_DIR / "ADR-TEMPLATE.zh.md").exists(), "缺少 ADR-TEMPLATE.zh.md"


@pytest.mark.parametrize("path", _adr_files(), ids=lambda p: p.name)
def test_filename_matches_convention(path: Path):
    """对应 README：英文 YYYY-MM-DD-NNNN-标题.md，中文 YYYY-MM-DD-NNNN-标题.zh.md"""
    assert ADR_FILENAME_RE.match(path.name), (
        f"{path.name} 不符合命名约定 YYYY-MM-DD-NNNN-标题.md（中文版为 .zh.md）"
    )


def test_every_adr_has_bilingual_pair():
    """对应 README：每份 ADR 必须同时有英文 .md 和中文 .zh.md"""
    files = _adr_files()
    keys = set()
    langs_by_key: dict[str, set[str]] = {}
    for f in files:
        m = ADR_FILENAME_RE.match(f.name)
        key = f"{m.group('date')}-{m.group('num')}-{m.group('slug')}"
        langs_by_key.setdefault(key, set()).add(m.group("lang") or "en")
        keys.add(key)

    missing = []
    for key, langs in langs_by_key.items():
        if langs != {"en", "zh"}:
            missing.append((key, langs))

    assert not missing, f"以下 ADR 缺少中英文其中一份: {missing}"


def test_adr_numbers_are_sequential_no_gaps_no_duplicates():
    """对应 README：编号四位数字，连续递增，不跳号不重复"""
    files = _adr_files()
    numbers = sorted({int(ADR_FILENAME_RE.match(f.name).group("num")) for f in files})

    if not numbers:
        pytest.skip("还没有任何 ADR，跳过编号连续性检查")

    expected = list(range(1, len(numbers) + 1))
    assert numbers == expected, (
        f"ADR 编号不连续或有跳号/重复：实际 {numbers}，期望 {expected}"
    )


@pytest.mark.parametrize("path", _adr_files(), ids=lambda p: p.name)
def test_required_sections_present(path: Path):
    """对应 README：Nygard 格式的四个必需章节都要出现"""
    content = path.read_text(encoding="utf-8")
    missing = [s for s in REQUIRED_SECTIONS if s not in content]
    assert not missing, f"{path.name} 缺少必需章节：{missing}"


@pytest.mark.parametrize("path", _adr_files(), ids=lambda p: p.name)
def test_status_value_is_valid(path: Path):
    """对应 README「状态流转」一节：Status 只能是四种取值之一"""
    content = path.read_text(encoding="utf-8")
    m = re.search(r"[-*]?\s*Status:\s*(.+)", content)
    assert m, f"{path.name} 没有找到 Status 字段"
    status_line = m.group(1).strip()
    assert status_line.startswith(VALID_STATUS_PREFIXES), (
        f"{path.name} 的 Status 值 '{status_line}' 不是合法取值 "
        f"{VALID_STATUS_PREFIXES}"
    )


def test_agents_md_adr_links_resolve():
    """AGENTS.md 里的架构决策链接必须指向真实存在的文件，防止改名后忘了同步更新"""
    if not AGENTS_MD.exists():
        pytest.skip("AGENTS.md 不存在，跳过")

    content = AGENTS_MD.read_text(encoding="utf-8")
    # 匹配形如 [ADR-0001](docs/decisions/xxx.md) 的 markdown 链接
    links = re.findall(r"\]\((docs/decisions/[^\)]+\.md)\)", content)

    broken = [link for link in links if not (REPO_ROOT / link).exists()]
    assert not broken, f"AGENTS.md 里以下 ADR 链接指向不存在的文件：{broken}"
