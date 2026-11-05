from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest
from builders import Git


@pytest.fixture
def git(tmp_path: Path) -> Git:
    """A real repository in tmp_path, on `main`, with one empty commit."""
    env = {
        **os.environ,
        "GIT_AUTHOR_NAME": "test",
        "GIT_AUTHOR_EMAIL": "test@example.invalid",
        "GIT_COMMITTER_NAME": "test",
        "GIT_COMMITTER_EMAIL": "test@example.invalid",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_NOSYSTEM": "1",
    }

    def run(*args: str) -> str:
        result = subprocess.run(
            ["git", *args], cwd=tmp_path, env=env, capture_output=True, text=True, check=True
        )
        return result.stdout

    run("init", "-q", "-b", "main")
    run("commit", "-q", "--allow-empty", "-m", "base")
    return run
