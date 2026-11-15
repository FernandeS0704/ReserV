from src.salas import cadastrar_sala, formatar_listagem, listar_salas
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
    print("3 - Realizar reserva")
    print("4 - Cancelar reserva")
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
            opcao_realizar_reserva()
        elif opcao == "4":
            opcao_cancelar_reserva()
        elif opcao == "0":
            print("Encerrando o sistema.")
            break
        else:
            print("Opção inválida. Tente novamente.")