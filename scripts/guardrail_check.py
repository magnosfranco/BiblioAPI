#!/usr/bin/env python3
"""Guardrail determinístico da BiblioAPI (Python puro — Windows/Linux/macOS).

Estágio A (GUARDRAIL_STAGE=A): bloqueia comandos destrutivos, segredos e e-mails não sintéticos.
Estágio B é o padrão: também exige plano aprovado para editar app/ ou mcp_server/.

Protocolo Cursor hooks: JSON em stdin; JSON em stdout com permission allow|deny.
Exit 0 = sucesso; exit 2 = bloqueio explícito.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parents[1]
STAGE = os.environ.get("GUARDRAIL_STAGE", "B").upper()

DESTRUCTIVE_PATTERNS = [
    re.compile(r"\brm\s+-rf\b", re.I),
    re.compile(r"\bgit\s+push\s+.*--force\b", re.I),
    re.compile(r"\bgit\s+push\s+-f\b", re.I),
    re.compile(r"\bDROP\s+TABLE\b", re.I),
    # CLI sqlite3 no shell (imports em app/db.py e app/service.py são tratados em check_sqlite3_boundary)
    re.compile(r"(^|[;&|]\s*)sqlite3\b", re.I),
]

SECRET_PATTERNS = [
    re.compile(r"(^|/|\\)\.env(\.|$|/|\\)", re.I),
    re.compile(r"\bsk-[A-Za-z0-9]{10,}\b"),
    re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bBearer\s+[A-Za-z0-9\-._~+/]+=*\b"),
]

EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
SYNTHETIC_EMAIL_DOMAIN = "@biblioteca.example.com"

SQLITE3_ALLOWED = {
    "app/db.py",
    "app/service.py",
}
SQLITE3_IMPORT = re.compile(r"(^|\n)\s*(import\s+sqlite3|from\s+sqlite3\s+import)\b")


def _respond(permission: str, message: str, exit_code: int = 0) -> int:
    payload = {
        "permission": permission,
        "user_message": message,
        "agent_message": message,
    }
    sys.stdout.write(json.dumps(payload, ensure_ascii=False))
    sys.stdout.flush()
    return exit_code


def _deny(message: str) -> int:
    return _respond("deny", message, exit_code=2)


def _allow(message: str = "ok") -> int:
    return _respond("allow", message, exit_code=0)


def _as_repo_relative(path: str | None) -> str | None:
    if not path:
        return None
    p = Path(path)
    try:
        if p.is_absolute():
            return p.resolve().relative_to(REPO_ROOT).as_posix()
    except Exception:
        pass
    return path.replace("\\", "/").lstrip("./")


def _collect_text(payload: dict[str, Any]) -> str:
    chunks: list[str] = []
    for key in ("command", "content", "new_string", "old_string", "prompt"):
        val = payload.get(key)
        if isinstance(val, str):
            chunks.append(val)
    tool_input = payload.get("tool_input") or payload.get("input") or {}
    if isinstance(tool_input, dict):
        for key in ("command", "content", "new_string", "old_string", "contents", "file_path", "path"):
            val = tool_input.get(key)
            if isinstance(val, str):
                chunks.append(val)
    return "\n".join(chunks)


def _file_path(payload: dict[str, Any]) -> str | None:
    for key in ("file_path", "path"):
        if isinstance(payload.get(key), str):
            return _as_repo_relative(payload[key])
    tool_input = payload.get("tool_input") or payload.get("input") or {}
    if isinstance(tool_input, dict):
        for key in ("file_path", "path"):
            if isinstance(tool_input.get(key), str):
                return _as_repo_relative(tool_input[key])
    return None


def _plans_dir() -> Path:
    override = os.environ.get("GUARDRAIL_PLANS_DIR")
    if override:
        return Path(override)
    return REPO_ROOT / "docs" / "plans"


def _plan_approved() -> bool:
    plans = _plans_dir()
    if not plans.is_dir():
        return False
    for plan in plans.glob("*.md"):
        text = plan.read_text(encoding="utf-8", errors="ignore")
        if re.search(r"Decisão humana:\s*aceita", text, re.I) and not re.search(
            r"\|\s*pendente\s*\|", text, re.I
        ):
            # Estágio B exige pelo menos um plano aceito e nenhum pendente no arquivo tocado;
            # simplificação G0: qualquer plano aceito libera — refinado na Etapa 3.
            if "pendente" in text.lower() and "decisão humana: aceita" not in text.lower():
                continue
            return True
    return False


def _has_pending_plans_blocking(path: str | None) -> bool:
    """Estágio B: editar app/ ou mcp_server/ exige plano aprovado sem 'pendente'."""
    if not path:
        return False
    norm = path.replace("\\", "/")
    if not (norm.startswith("app/") or norm.startswith("mcp_server/")):
        return False
    plans = _plans_dir()
    if not plans.is_dir():
        return True
    approved = False
    for plan in plans.glob("*.md"):
        text = plan.read_text(encoding="utf-8", errors="ignore")
        if re.search(r"\|\s*pendente\s*\|", text, re.I):
            return True
        if re.search(r"Decisão humana:\s*aceita", text, re.I):
            approved = True
    return not approved


def check_destructive(text: str) -> str | None:
    for pat in DESTRUCTIVE_PATTERNS:
        if pat.search(text):
            return f"Bloqueado (Estágio {STAGE}): comando/padrão destrutivo detectado ({pat.pattern})."
    return None


def check_secrets(text: str, path: str | None) -> str | None:
    if path and path.replace("\\", "/").endswith(".env"):
        return "Bloqueado: escrita/leitura de arquivo .env não permitida ao agente."
    for pat in SECRET_PATTERNS:
        if pat.search(text):
            return "Bloqueado: possível segredo detectado (sk-/ghp_/Bearer/.env)."
    return None


def check_emails(text: str, path: str | None) -> str | None:
    if not path:
        return None
    norm = path.replace("\\", "/")
    if not (norm.startswith("tests/") or "/fixtures" in norm or norm.endswith(".feature")):
        return None
    for email in EMAIL_PATTERN.findall(text):
        if not email.lower().endswith(SYNTHETIC_EMAIL_DOMAIN):
            return (
                f"Bloqueado: e-mail não sintético '{email}'. "
                f"Use o domínio {SYNTHETIC_EMAIL_DOMAIN}."
            )
    return None


def check_sqlite3_boundary(text: str, path: str | None) -> str | None:
    if not path:
        return None
    norm = path.replace("\\", "/")
    if not SQLITE3_IMPORT.search(text):
        return None
    if norm in SQLITE3_ALLOWED:
        return None
    return (
        "Bloqueado: sqlite3 só é permitido em app/db.py e app/service.py "
        f"(arquivo: {norm})."
    )


def evaluate(payload: dict[str, Any]) -> int:
    text = _collect_text(payload)
    path = _file_path(payload)
    command = ""
    if isinstance(payload.get("command"), str):
        command = payload["command"]
    tool_input = payload.get("tool_input") or payload.get("input") or {}
    if isinstance(tool_input, dict) and isinstance(tool_input.get("command"), str):
        command = tool_input["command"]

    for checker in (
        lambda: check_destructive(command),  # só comando de shell — não o corpo do arquivo
        lambda: check_secrets(text, path),
        lambda: check_emails(text, path),
        lambda: check_sqlite3_boundary(text, path),
    ):
        reason = checker()
        if reason:
            return _deny(reason)

    if STAGE == "B" and _has_pending_plans_blocking(path):
        return _deny(
            "Bloqueado (Estágio B): edições em app/ ou mcp_server/ exigem "
            "plano em docs/plans/ com 'Decisão humana: aceita' e sem linhas pendentes."
        )

    return _allow()


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    raw = sys.stdin.read() if not sys.stdin.isatty() else ""
    if not raw.strip():
        # Modo CLI de smoke: python scripts/guardrail_check.py --self-test
        if argv and argv[0] == "--self-test":
            samples = [
                ({"command": "rm -rf /"}, True),
                ({"command": "pytest -q"}, False),
                (
                    {
                        "tool_input": {
                            "file_path": "tests/test_x.py",
                            "content": "email = 'a@gmail.com'",
                        }
                    },
                    True,
                ),
                (
                    {
                        "tool_input": {
                            "file_path": "tests/test_x.py",
                            "content": "email = 'a@biblioteca.example.com'",
                        }
                    },
                    False,
                ),
            ]
            failures = 0
            for sample, should_deny in samples:
                # Captura via evaluate indireta
                code = 0
                try:
                    # reimplementação leve: chamar evaluate e inferir pelo return
                    from contextlib import redirect_stdout
                    from io import StringIO

                    buf = StringIO()
                    with redirect_stdout(buf):
                        code = evaluate(sample)
                    denied = code == 2
                    if denied != should_deny:
                        failures += 1
                        print(f"FAIL sample={sample} expected_deny={should_deny} got={denied}", file=sys.stderr)
                except Exception as exc:  # pragma: no cover
                    failures += 1
                    print(f"ERROR {exc}", file=sys.stderr)
            print("self-test ok" if failures == 0 else f"self-test failures={failures}")
            return 0 if failures == 0 else 1
        return _allow("stdin vazio")

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return _deny("Bloqueado: entrada do hook não é JSON válido.")

    if not isinstance(payload, dict):
        return _deny("Bloqueado: payload do hook inválido.")

    return evaluate(payload)


if __name__ == "__main__":
    raise SystemExit(main())
