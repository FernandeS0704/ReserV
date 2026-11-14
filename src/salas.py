from src import armazenamento


def _texto_preenchido(valor):
    return isinstance(valor, str) and bool(valor.strip())


def cadastrar_sala(nome, capacidade, localizacao):
    if not _texto_preenchido(nome):
        raise ValueError("O nome da sala é obrigatório.")

    if not _texto_preenchido(localizacao):
        raise ValueError("A localização da sala é obrigatória.")

    if not isinstance(capacidade, int) or capacidade <= 0:
        raise ValueError("A capacidade deve ser um número inteiro maior que zero.")

    sala = {
        "id": armazenamento.gerar_id(),
        "nome": nome,
        "capacidade": capacidade,
        "localizacao": localizacao,
    }
    armazenamento.salas.append(sala)
    return sala