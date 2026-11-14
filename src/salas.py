from src import armazenamento


def cadastrar_sala(nome, capacidade, localizacao):
    if not isinstance(nome, str) or not nome.strip():
        raise ValueError("O nome da sala é obrigatório.")

    if not isinstance(localizacao, str) or not localizacao.strip():
        raise ValueError("A localização da sala é obrigatória.")

    if not isinstance(capacidade, int) or capacidade <= 0:
        raise ValueError("A capacidade deve ser um número inteiro maior que zero.")

    sala = {
        "id": len(armazenamento.salas) + 1,
        "nome": nome,
        "capacidade": capacidade,
        "localizacao": localizacao,
    }
    armazenamento.salas.append(sala)
    return sala