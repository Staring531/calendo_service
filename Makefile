.DEFAULT_GOAL := help
.PHONY: sync add remove lint format typecheck test cov build clean check help

## 安装/同步依赖（含 dev 依赖）
sync:
	uv sync --all-extras

## 添加依赖，例如：make add pkg=httpx
add:
	uv add $(pkg)

## 添加 dev 依赖，例如：make add-dev pkg=pytest
add-dev:
	uv add --dev $(pkg)

## 移除依赖，例如：make remove pkg=httpx
remove:
	uv remove $(pkg)

## ruff 检查（含 import 排序）
lint:
	uv run ruff check .

## ruff 自动修复 + 格式化
format:
	uv run ruff check --fix .
	uv run ruff format .

## mypy 类型检查
typecheck:
	uv run mypy src

## 跑测试
test:
	uv run pytest

## 跑测试并生成覆盖率报告
cov:
	uv run pytest --cov=src --cov-report=html
	@echo "打开 htmlcov/index.html 查看报告"

## lint + typecheck + test 一次性跑完，适合提交前 / CI 用
check: lint typecheck test

## 构建 wheel / sdist
build:
	uv build

## 清理构建产物和缓存
clean:
	rm -rf dist/ build/ *.egg-info htmlcov/ .pytest_cache/ .mypy_cache/ .ruff_cache/
	find . -type d -name "__pycache__" -exec rm -rf {} +

## 显示帮助
help:
	@grep -E '^## .*|^[a-zA-Z_-]+:' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":"} /^## / {desc=substr($$0,4)} /^[a-zA-Z_-]+:/ {printf "\033[36m%-14s\033[0m %s\n", $$1, desc}'
