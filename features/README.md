# features/ — cenários BDD (RM1)

## Papel nesta fase (C1)

**Especificação**, não suíte executável da API ainda.

Os arquivos `*.feature` descrevem o comportamento esperado (Gherkin).  
No C1 o CI valida presença e quantidade de cenários via `tests/test_artefatos.py`.  
A ligação `pytest-bdd` → `app/` ocorre **depois** que o código existir (pós-RM1 temporal).

| Campo | Valor |
| :--- | :--- |
| Decisão | BDD no C1 = especificação pré-código |
| Aprovado por | Magno da Silva Franco |
| Data | 2026-11-22 |
| Base | `Projeto.pdf` RM1 — cenários BDD escritos **ANTES do código** |
