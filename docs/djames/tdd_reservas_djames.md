# TDD — Reservas

Os ciclos foram feitos no repositório local. Os prints mostram as execuções reais do pytest em cada etapa.

## Realizar reserva

- Red da reserva válida: [tdd_reserva_red.png](evidencias/tdd_reserva_red.png)
- Green da reserva válida: [tdd_reserva_green.png](evidencias/tdd_reserva_green.png)
- Red e Green para sala inexistente: [Red](evidencias/tdd_sala_inexistente_red.png), [Green](evidencias/tdd_sala_inexistente_green.png)
- Red, Green e Refactor para campos obrigatórios: [Red](evidencias/tdd_campos_obrigatorios_red.png), [Green](evidencias/tdd_campos_obrigatorios_green.png), [Refactor](evidencias/tdd_campos_obrigatorios_refactor.png)
- Red, Green e Refactor para conflito de horário: [Red](evidencias/tdd_conflito_red.png), [Green](evidencias/tdd_conflito_green.png), [Refactor](evidencias/tdd_conflito_refactor.png)

## Cancelar reserva

- Red, Green e Refactor para cancelamento, ID inexistente e repetição: [Red](evidencias/tdd_cancelamento_red.png), [Green](evidencias/tdd_cancelamento_green.png), [Refactor](evidencias/tdd_cancelamento_refactor.png)

## Suíte completa

A suíte completa foi executada com `python -m pytest -v`: **40 testes passaram**. A captura está em [suite_reservas_djames.png](evidencias/suite_reservas_djames.png).
