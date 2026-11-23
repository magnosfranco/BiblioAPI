# Relatório — eval de disparo da skill auditar-biblioapi (RM5)

Runner: `evals/run_skill_eval.py`. Sem modelo de linguagem.
Casos: 10 (5 positivos e 5 negativos).

| Versão | VP | FP | FN | VN | Precisão | Recall | F1 |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| v1 (larga) | 5 | 4 | 0 | 1 | 0.56 | 1.00 | 0.71 |
| v2 (com fronteira) | 5 | 0 | 0 | 5 | 1.00 | 1.00 | 1.00 |

A v1 cita Docker, CI e Git na description, então esses pedidos disparam a skill (falsos positivos).
A v2 mantém as regras de negócio e acrescenta `Não use para Docker, CI, Git, certificado, formatação ou infraestrutura`.
O F1 sobe de 0.71 para 1.00. O arquivo da skill versiona a v2.
