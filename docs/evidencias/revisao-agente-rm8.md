# Evidência — revisão por agente (RM8)

| Campo | Valor |
| :--- | :--- |
| Data | 2026-11-23 |
| Revisor | `spec-reviewer` (`.cursor/agents/spec-reviewer.md`) |
| Regra dos próximos PRs | `.cursor/rules/revisao-pr-rm8.mdc` (sempre ativa) |

O agente publica um comentário no PR e para. Magno responde cada comentário. Sem essa resposta o RM8 do PR não fecha. Bloqueio vira issue nova.

## Amostra nos PRs já mergeados

| PR | Veredito | Comentário | Resposta humana |
| :--- | :--- | :--- | :--- |
| [#10](https://github.com/magnosfranco/BiblioAPI/pull/10) empréstimos | LGTM | [comentário](https://github.com/magnosfranco/BiblioAPI/pull/10#issuecomment-7117264860) | Pendente |
| [#13](https://github.com/magnosfranco/BiblioAPI/pull/13) MCP próprio | LGTM | [comentário](https://github.com/magnosfranco/BiblioAPI/pull/13#issuecomment-7117266212) | Pendente |
| [#17](https://github.com/magnosfranco/BiblioAPI/pull/17) recomendações | LGTM condicional | [comentário](https://github.com/magnosfranco/BiblioAPI/pull/17#issuecomment-7117267783) | Pendente |

A sugestão do #17 (modelo `qwen2.5:7b` e timeout de 2 s) já foi tratada no PR #19. O #17 não reabre.
