# BDD — Reservas

Os seis cenários Gherkin estão em `tests/features/reservas.feature` e cobrem reservar, sala inexistente, conflito, cancelar, ID inexistente e cancelamento repetido.

## Red — concluído

O arquivo temporário `tests/test_bdd_reservas_red.py` carrega os cenários sem implementar os passos.

Rode:

```powershell
python -m pytest tests/test_bdd_reservas_red.py -v
```

O Red foi executado antes da implementação dos passos, usando temporariamente apenas o carregamento dos cenários. O arquivo temporário foi removido após a captura: [bdd_reservas_red.png](evidencias/bdd_reservas_red.png).

## Green

Os passos reais do projeto estão em `tests/test_bdd_reservas.py`.

Rode:

```powershell
python -m pytest tests/test_bdd_reservas.py -v
```

Os seis cenários passaram. A captura está em [bdd_reservas_green.png](evidencias/bdd_reservas_green.png).
