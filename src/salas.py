from src import armazenamento


def cadastrar_sala(nome, capacidade, localizacao):
    sala = {
        "id": len(armazenamento.salas) + 1,  # id provisório (melhoramos depois)
        "nome": nome,
        "capacidade": capacidade,
        "localizacao": localizacao,
    }
    armazenamento.salas.append(sala)
    return sala