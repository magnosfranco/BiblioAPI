"""Testes do guardrail — Estágio A (Gate G0)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "guardrail_check.py"


def _run(payload: dict) -> tuple[int, dict]:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=str(ROOT),
        check=False,
    )
    body = proc.stdout.strip() or "{}"
    data = json.loads(body)
    return proc.returncode, data


def test_allows_safe_pytest_command():
    code, data = _run({"command": "pytest -q"})
    assert code == 0
    assert data["permission"] == "allow"


def test_blocks_rm_rf():
    code, data = _run({"command": "rm -rf /tmp/x"})
    assert code == 2
    assert data["permission"] == "deny"


def test_blocks_force_push():
    code, data = _run({"command": "git push --force origin main"})
    assert code == 2
    assert data["permission"] == "deny"


def test_blocks_sqlite3_cli():
    code, data = _run({"command": "sqlite3 biblio.db '.tables'"})
    assert code == 2
    assert data["permission"] == "deny"


def test_blocks_non_synthetic_email_in_tests():
    code, data = _run(
        {
            "tool_input": {
                "file_path": "tests/test_example.py",
                "content": "email = 'pessoa@gmail.com'",
            }
        }
    )
    assert code == 2
    assert data["permission"] == "deny"


def test_allows_synthetic_email_in_tests():
    code, data = _run(
        {
            "tool_input": {
                "file_path": "tests/test_example.py",
                "content": "email = 'ana@biblioteca.example.com'",
            }
        }
    )
    assert code == 0
    assert data["permission"] == "allow"


def test_blocks_sqlite3_import_outside_allowed_files():
    code, data = _run(
        {
            "tool_input": {
                "file_path": "app/routes.py",
                "content": "import sqlite3\n",
            }
        }
    )
    assert code == 2
    assert data["permission"] == "deny"


def test_allows_sqlite3_import_in_service():
    code, data = _run(
        {
            "tool_input": {
                "file_path": "app/service.py",
                "content": "import sqlite3\n",
            }
        }
    )
    assert code == 0
    assert data["permission"] == "allow"


def test_stage_a_does_not_require_plan_for_app_edit():
    """Estágio A: editar app/ sem plano ainda é permitido (fatia vibe)."""
    code, data = _run(
        {
            "tool_input": {
                "file_path": "app/service.py",
                "content": "def criar_socio():\n    return 1\n",
            }
        }
    )
    assert code == 0
    assert data["permission"] == "allow"
