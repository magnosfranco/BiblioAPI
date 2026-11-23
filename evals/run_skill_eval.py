"""Eval de disparo da skill auditar-biblioapi. Sem rede e sem LLM.

O gatilho é a description. A v2 declara 'Não use para …'. Se o pedido cai nessa
lista, a skill não dispara. Caso contrário, dispara quando o pedido compartilha
uma palavra de conteúdo com a description.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

CASES = Path(__file__).resolve().parent / "skill_trigger_cases.json"
RELATORIO = Path(__file__).resolve().parent / "relatorio_skill_trigger.md"
SKILL = REPO / ".agents" / "skills" / "auditar-biblioapi" / "SKILL.md"

STOP = {
    "para", "com", "uma", "que", "dos", "das", "não", "nao", "use", "quando",
    "sobre", "pelo", "pela", "este", "esta", "qualquer", "pedido", "como",
    "faz", "fazer", "está", "esta", "são", "sao",
}


def tokens(texto: str) -> set[str]:
    palavras = re.findall(r"[A-Za-zÀ-ÿ0-9]{2,}", texto.lower())
    return {p for p in palavras if p not in STOP}


def negativos(description: str) -> set[str]:
    match = re.search(r"não use para (.+)$", description, re.I)
    if not match:
        return set()
    return tokens(match.group(1))


def dispara(description: str, prompt: str) -> bool:
    proibidos = negativos(description)
    pedido = tokens(prompt)
    if proibidos and pedido & proibidos:
        return False
    return bool(pedido & tokens(description))


def metricas(description: str, casos: list[dict]) -> dict[str, float | int]:
    vp = fp = fn = vn = 0
    for caso in casos:
        previsto = dispara(description, caso["prompt"])
        esperado = bool(caso["esperado"])
        if previsto and esperado:
            vp += 1
        elif previsto and not esperado:
            fp += 1
        elif not previsto and esperado:
            fn += 1
        else:
            vn += 1
    precisao = vp / (vp + fp) if vp + fp else 0.0
    recall = vp / (vp + fn) if vp + fn else 0.0
    f1 = 2 * precisao * recall / (precisao + recall) if precisao + recall else 0.0
    return {
        "vp": vp,
        "fp": fp,
        "fn": fn,
        "vn": vn,
        "precisao": precisao,
        "recall": recall,
        "f1": f1,
    }


def avaliar() -> dict:
    dados = json.loads(CASES.read_text(encoding="utf-8"))
    return {
        "v1": metricas(dados["v1_description"], dados["casos"]),
        "v2": metricas(dados["v2_description"], dados["casos"]),
        "n": len(dados["casos"]),
    }


def _fmt(valor: float) -> str:
    return f"{valor:.2f}"


def render(resultado: dict) -> str:
    v1, v2 = resultado["v1"], resultado["v2"]
    linhas = [
        "# Relatório — eval de disparo da skill auditar-biblioapi (RM5)",
        "",
        "Runner: `evals/run_skill_eval.py`. Sem modelo de linguagem.",
        f"Casos: {resultado['n']} (5 positivos e 5 negativos).",
        "",
        "| Versão | VP | FP | FN | VN | Precisão | Recall | F1 |",
        "| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        (
            f"| v1 (larga) | {v1['vp']} | {v1['fp']} | {v1['fn']} | {v1['vn']} | "
            f"{_fmt(v1['precisao'])} | {_fmt(v1['recall'])} | {_fmt(v1['f1'])} |"
        ),
        (
            f"| v2 (com fronteira) | {v2['vp']} | {v2['fp']} | {v2['fn']} | {v2['vn']} | "
            f"{_fmt(v2['precisao'])} | {_fmt(v2['recall'])} | {_fmt(v2['f1'])} |"
        ),
        "",
        "A v1 cita Docker, CI e Git na description, então esses pedidos disparam a skill (falsos positivos).",
        "A v2 mantém as regras de negócio e acrescenta `Não use para Docker, CI, Git, certificado, formatação ou infraestrutura`.",
        f"O F1 sobe de {_fmt(v1['f1'])} para {_fmt(v2['f1'])}. O arquivo da skill versiona a v2.",
        "",
    ]
    return "\n".join(linhas)


def main() -> None:
    texto = render(avaliar())
    RELATORIO.write_text(texto, encoding="utf-8")
    description = ""
    bruto = SKILL.read_text(encoding="utf-8")
    match = re.search(r"description:\s*>\s*(.*?)\n---", bruto, re.S)
    if match:
        description = " ".join(match.group(1).split())
    dados = json.loads(CASES.read_text(encoding="utf-8"))
    v2 = " ".join(dados["v2_description"].split())
    if description != v2:
        raise SystemExit("SKILL.md não está na description v2")
    if avaliar()["v2"]["f1"] <= avaliar()["v1"]["f1"]:
        raise SystemExit(texto)
    print(texto)


if __name__ == "__main__":
    main()
