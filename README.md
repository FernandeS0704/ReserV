# ReserV — Sistema de Agendamento e Reserva de Salas

Sistema de terminal em Python para cadastro e gerenciamento de salas e reservas. Os dados ficam em memória e são apagados ao encerrar o programa.

## Funcionalidades e responsáveis

### Implementadas

| Integrante | Funcionalidades |
|---|---|
| Arthur — Integrante 1 | Cadastrar salas e listar salas cadastradas. O cadastro valida nome, capacidade e localização. |
| Vitor — Integrante 2 | Editar salas e excluir salas. A exclusão é bloqueada quando há reservas futuras ativas. |
| Djames — Integrante 3 | Realizar reservas e cancelar reservas. O sistema valida sala, campos obrigatórios e conflito de horário. |

### Planejadas

| Integrantes | Funcionalidades |
|---|---|
| Gustavo e Pedro | Consultar a disponibilidade das salas por data e horário; listar reservas com sala, data e horário. A divisão dessas duas tarefas entre eles ainda será combinada. |

As consultas ainda serão implementadas. Os cenários, testes e opções de menu correspondentes serão adicionados seguindo a estrutura já usada nas partes de Arthur, Vitor e Djames.

## Requisitos

- Python 3.10 ou superior
- Dependências `pytest` e `pytest-bdd`, listadas em `requirements.txt`

## Instalação no Windows

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

No Linux ou macOS, ative o ambiente com `source venv/bin/activate`.

## Executar o sistema

```powershell
python main.py
```

Opções atuais do menu:

```text
1 - Cadastrar sala
2 - Listar salas
3 - Editar sala
4 - Excluir sala
5 - Realizar reserva
6 - Cancelar reserva
0 - Sair
```

## Executar os testes

```powershell
python -m pytest -v
python -m pytest tests/test_cadastro_salas.py -v
python -m pytest tests/test_listagem_salas.py -v
python -m pytest tests/test_edicao_salas.py -v
python -m pytest tests/test_exclusao_salas.py -v
python -m pytest tests/test_reservas.py -v
python -m pytest tests/test_cancelamento_reservas.py -v
python -m pytest tests/test_integracao_reservas_exclusao.py -v
python -m pytest tests/test_bdd_salas.py -v
python -m pytest tests/test_bdd_edicao_exclusao.py -v
python -m pytest tests/test_bdd_reservas.py -v
```

## Estrutura principal

```text
main.py
src/
  armazenamento.py
  salas.py
  reservas.py
  interface.py
tests/
  test_cadastro_salas.py
  test_listagem_salas.py
  test_edicao_salas.py
  test_exclusao_salas.py
  test_reservas.py
  test_cancelamento_reservas.py
  test_integracao_reservas_exclusao.py
  test_bdd_salas.py
  test_bdd_edicao_exclusao.py
  test_bdd_reservas.py
  features/
docs/
  arthur/
  vitor/
  djames/
```

Cada parte mantém seu relatório TDD/BDD e suas evidências na pasta correspondente em `docs/`. As consultas de Gustavo e Pedro ainda não têm arquivos de implementação.

## Dados compartilhados

- Salas: `armazenamento.salas`, com `id`, `nome`, `capacidade` e `localizacao`.
- Reservas: `armazenamento.reservas`, com `id`, `sala_id`, `responsavel`, `data`, `horario` e `status`.
- Os IDs são gerados por `armazenamento.gerar_id()` e `armazenamento.gerar_id_reserva()` e são reiniciados nos testes por `armazenamento.reiniciar()`.
