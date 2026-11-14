from src import armazenamento


def _texto_preenchido(valor):
    return isinstance(valor, str) and bool(valor.strip())


def _capacidade_valida(valor):
    return isinstance(valor, int) and valor > 0


def cadastrar_sala(nome, capacidade, localizacao):
    if not _texto_preenchido(nome):
        raise ValueError("O nome da sala é obrigatório.")

    if not _texto_preenchido(localizacao):
        raise ValueError("A localização da sala é obrigatória.")

    if not _capacidade_valida(capacidade):
        raise ValueError("A capacidade deve ser um número inteiro maior que zero.")

    sala = {
        "id": armazenamento.gerar_id(),
        "nome": nome,
        "capacidade": capacidade,
        "localizacao": localizacao,
    }
    armazenamento.salas.append(sala)
    return sala

def listar_salas():
    return list(armazenamento.salas)