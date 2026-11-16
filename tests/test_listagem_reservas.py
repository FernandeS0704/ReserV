from src import armazenamento
from src.consultas import formatar_reservas, listar_reservas
from src.reservas import cancelar_reserva, realizar_reserva
from src.salas import cadastrar_sala, excluir_sala


def test_listar_reservas_sem_nenhuma_realizada():
    assert listar_reservas() == []


def test_listar_reservas_mostra_dados_da_sala_data_e_horario():
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")
    reserva = realizar_reserva(sala["id"], "Pedro", "20/11/2026", "19:00-20:00")

    resultado = listar_reservas()

    assert resultado == [
        {
            "id": reserva["id"],
            "sala_id": sala["id"],
            "sala_nome": "Sala 01",
            "sala_localizacao": "Bloco A",
            "responsavel": "Pedro",
            "data": "20/11/2026",
            "horario": "19:00-20:00",
            "status": "ativa",
        }
    ]


def test_listar_reservas_na_ordem_em_que_foram_realizadas():
    sala1 = cadastrar_sala("Sala 01", 20, "Bloco A")
    sala2 = cadastrar_sala("Laboratório", 15, "Bloco C")
    realizar_reserva(sala2["id"], "Pedro", "21/11/2026", "08:00-10:00")
    realizar_reserva(sala1["id"], "Djames", "20/11/2026", "19:00-20:00")

    resultado = listar_reservas()

    assert [r["id"] for r in resultado] == [1, 2]
    assert [r["sala_nome"] for r in resultado] == ["Laboratório", "Sala 01"]


def test_listar_reservas_inclui_reservas_canceladas_com_status():
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")
    reserva = realizar_reserva(sala["id"], "Pedro", "20/11/2026", "19:00-20:00")
    cancelar_reserva(reserva["id"])

    resultado = listar_reservas()

    assert len(resultado) == 1
    assert resultado[0]["status"] == "cancelada"


def test_alterar_listagem_nao_altera_reservas_guardadas():
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")
    realizar_reserva(sala["id"], "Pedro", "20/11/2026", "19:00-20:00")

    resultado = listar_reservas()
    resultado[0]["responsavel"] = "Outra pessoa"
    resultado.clear()

    assert len(armazenamento.reservas) == 1
    assert armazenamento.reservas[0]["responsavel"] == "Pedro"


def test_listar_reserva_de_sala_que_foi_excluida():
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")
    realizar_reserva(sala["id"], "Pedro", "10/01/2025", "19:00-20:00")
    excluir_sala(sala["id"])

    resultado = listar_reservas()

    assert len(resultado) == 1
    assert resultado[0]["sala_id"] == sala["id"]
    assert resultado[0]["sala_nome"] == "Sala removida"
    assert resultado[0]["sala_localizacao"] == "-"


def test_formatar_reservas_sem_reservas_informa_que_nao_ha_reservas():
    texto = formatar_reservas([])

    assert "não há reservas realizadas" in texto.lower()


def test_formatar_reservas_mostra_sala_data_e_horario():
    sala1 = cadastrar_sala("Sala 01", 20, "Bloco A")
    sala2 = cadastrar_sala("Laboratório de Informática", 35, "Bloco B")
    realizar_reserva(sala1["id"], "Pedro", "20/11/2026", "19:00-20:00")
    realizar_reserva(sala2["id"], "Djames", "21/11/2026", "08:00-10:00")

    linhas = formatar_reservas(listar_reservas()).splitlines()

    for titulo in ["ID", "Sala", "Localização", "Responsável", "Data", "Horário", "Status"]:
        assert titulo in linhas[0]

    assert len(linhas) == 4

    for texto in ["1", "Sala 01", "Bloco A", "Pedro", "20/11/2026", "19:00-20:00", "ativa"]:
        assert texto in linhas[2]
    for texto in ["2", "Laboratório de Informática", "Bloco B", "Djames", "21/11/2026", "08:00-10:00"]:
        assert texto in linhas[3]


def test_formatar_reservas_alinha_as_colunas():
    sala1 = cadastrar_sala("Sala 01", 20, "Bloco A")
    sala2 = cadastrar_sala("Laboratório de Informática", 35, "Bloco B")
    realizar_reserva(sala1["id"], "Pedro", "20/11/2026", "19:00-20:00")
    realizar_reserva(sala2["id"], "Djames", "21/11/2026", "08:00-10:00")

    linhas = formatar_reservas(listar_reservas()).splitlines()

    posicao = linhas[0].index("Data")
    assert linhas[2].index("20/11/2026") == posicao
    assert linhas[3].index("21/11/2026") == posicao
