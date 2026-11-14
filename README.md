# ReserV — Sistema de Agendamento e Reserva de Salas

Sistema de terminal em Python para gerenciar salas e reservas. Este repositório contém a parte do **Integrante 1** (cadastro e listagem de salas), desenvolvida com TDD (pytest) e BDD (pytest-bdd).

## Funcionalidades desta parte

1. **Cadastrar sala:** nome, capacidade máxima e localização (todos obrigatórios; capacidade inteira maior que zero; id único gerado automaticamente).
2. **Listar salas:** exibe id, nome, capacidade e localização em uma tabela alinhada, ou informa que não há salas disponíveis.

Os dados ficam **somente em memória** e são perdidos ao fechar o programa.

## Requisitos

- Python 3.10 ou superior
- Dependências: `pytest` e `pytest-bdd` (listadas em `requirements.txt`)

## Instalação (Windows, PowerShell)

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Em Linux/Mac, ative o ambiente com `source venv/bin/activate`.

## Executar o sistema

```powershell
py main.py
```

Menu:

```
=== Sistema de Agendamento e Reserva de Salas ===
1 - Cadastrar sala
2 - Listar salas
0 - Sair
```

## Executar os testes

```powershell
py -m pytest -v                          # todos os testes (TDD e BDD)
py -m pytest tests\test_cadastro_salas.py -v
py -m pytest tests\test_listagem_salas.py -v
py -m pytest tests\test_bdd_salas.py -v  # cenários BDD
```

## Estrutura

```
main.py                      ponto de entrada
src/
  armazenamento.py           lista de salas em memória e gerador de id
  salas.py                   regras: cadastrar_sala, listar_salas, formatar_listagem
  interface.py               menu do terminal
tests/
  conftest.py                zera o armazenamento entre os testes
  test_cadastro_salas.py     testes TDD do cadastro
  test_listagem_salas.py     testes TDD da listagem
  test_bdd_salas.py          passos dos cenários BDD
  features/cadastro_salas.feature   cenários em Gherkin
docs/
  registro_tdd.md            registro dos ciclos TDD/BDD com evidências
```

## Para os outros integrantes

- Formato de cada sala: `{"id": int, "nome": str, "capacidade": int, "localizacao": str}`.
- Os dados ficam na lista `armazenamento.salas`. Acesse sempre por `from src import armazenamento` e `armazenamento.salas`.
- Para editar ou excluir uma sala, altere ou remova o item dessa lista. Os ids **não são reaproveitados**.
- `cadastrar_sala(nome, capacidade, localizacao)` devolve a sala criada ou levanta `ValueError` com mensagem clara.
- `listar_salas()` devolve uma cópia da lista; `formatar_listagem(lista)` devolve o texto da tabela.
- Para incluir novas opções no menu, edite `exibir_menu()` e `executar()` em `src/interface.py`.
