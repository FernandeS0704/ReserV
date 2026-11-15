from src.salas import (
    buscar_sala_por_id,
    cadastrar_sala,
    editar_sala,
    excluir_sala,
    formatar_listagem,
    listar_salas,
)
from src.reservas import cancelar_reserva, realizar_reserva


def _converter_inteiro(texto):
    try:
        return int(texto)
    except ValueError:
        return texto


def opcao_cadastrar_sala():
    print("\n--- Cadastrar sala ---")
    nome = input("Nome da sala: ")
    capacidade = _converter_inteiro(input("Capacidade máxima: ").strip())
    localizacao = input("Localização: ")

    try:
        sala = cadastrar_sala(nome, capacidade, localizacao)
    except ValueError as erro:
        print(f"Não foi possível cadastrar: {erro}")
    else:
        print(f"Sala cadastrada com sucesso! (id {sala['id']})")


def opcao_listar_salas():
    print("\n--- Salas cadastradas ---")
    print(formatar_listagem(listar_salas()))


def opcao_editar_sala():
    print("\n--- Editar sala ---")
    id_texto = input("ID da sala que deseja editar: ").strip()
    id_sala = _converter_inteiro(id_texto)

    try:
        sala_atual = buscar_sala_por_id(id_sala)
    except ValueError as erro:
        print(f"Não foi possível editar: {erro}")
        return

    print(
        f"Dados atuais -> Nome: {sala_atual['nome']} | "
        f"Capacidade: {sala_atual['capacidade']} | "
        f"Localização: {sala_atual['localizacao']}"
    )

    novo_nome = input("Novo nome (Enter para manter): ").strip()
    nova_cap = input("Nova capacidade (Enter para manter): ").strip()
    nova_loc = input("Nova localização (Enter para manter): ").strip()

    nome = novo_nome if novo_nome else None
    capacidade = _converter_inteiro(nova_cap) if nova_cap else None
    localizacao = nova_loc if nova_loc else None

    try:
        sala = editar_sala(
            id_sala, nome=nome, capacidade=capacidade, localizacao=localizacao
        )
    except ValueError as erro:
        print(f"Não foi possível editar: {erro}")
    else:
        print(f"Sala {sala['id']} atualizada com sucesso!")


def opcao_excluir_sala():
    print("\n--- Excluir sala ---")
    id_texto = input("ID da sala que deseja excluir: ").strip()
    id_sala = _converter_inteiro(id_texto)

    try:
        sala = buscar_sala_por_id(id_sala)
    except ValueError as erro:
        print(f"Não foi possível excluir: {erro}")
        return

    confirmacao = input(
        f"Deseja realmente excluir a sala '{sala['nome']}' (id {id_sala})? (s/n): "
    ).strip().lower()
    if confirmacao != "s":
        print("Operação cancelada.")
        return

    try:
        excluir_sala(id_sala)
    except ValueError as erro:
        print(f"Não foi possível excluir: {erro}")
    else:
        print(f"Sala {id_sala} excluída com sucesso!")


def opcao_realizar_reserva():
    print("\n--- Realizar reserva ---")
    sala_id = _converter_inteiro(input("ID da sala: ").strip())
    responsavel = input("Responsável: ")
    data = input("Data: ")
    horario = input("Horário: ")

    try:
        reserva = realizar_reserva(sala_id, responsavel, data, horario)
    except ValueError as erro:
        print(f"Não foi possível realizar a reserva: {erro}")
    else:
        print(f"Reserva realizada com sucesso! (id {reserva['id']})")


def opcao_cancelar_reserva():
    print("\n--- Cancelar reserva ---")
    reserva_id = _converter_inteiro(input("ID da reserva: ").strip())

    try:
        cancelar_reserva(reserva_id)
    except ValueError as erro:
        print(f"Não foi possível cancelar: {erro}")
    else:
        print("Reserva cancelada com sucesso!")


def exibir_menu():
    print("\n=== Sistema de Agendamento e Reserva de Salas ===")
    print("1 - Cadastrar sala")
    print("2 - Listar salas")
    print("3 - Editar sala")
    print("4 - Excluir sala")
    print("5 - Realizar reserva")
    print("6 - Cancelar reserva")
    print("0 - Sair")


def executar():
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            opcao_cadastrar_sala()
        elif opcao == "2":
            opcao_listar_salas()
        elif opcao == "3":
            opcao_editar_sala()
        elif opcao == "4":
            opcao_excluir_sala()
        elif opcao == "5":
            opcao_realizar_reserva()
        elif opcao == "6":
            opcao_cancelar_reserva()
        elif opcao == "0":
            print("Encerrando o sistema.")
            break
        else:
            print("Opção inválida. Tente novamente.")
