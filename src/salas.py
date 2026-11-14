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

# Títulos das colunas da tabela de listagem
TITULOS_LISTAGEM = ["ID", "Nome", "Capacidade", "Localização"]


def _calcular_larguras(titulos, linhas):
    """Devolve a largura de cada coluna: a do maior texto entre título e valores."""
    larguras = []
    for i, titulo in enumerate(titulos):
        valores = [len(linha[i]) for linha in linhas]
        larguras.append(max([len(titulo)] + valores))
    return larguras


def _montar_linha(colunas, larguras):
    """Junta as colunas de uma linha, preenchendo cada uma até a sua largura."""
    return "  ".join(
        coluna.ljust(largura) for coluna, largura in zip(colunas, larguras)
    ).rstrip()


def formatar_listagem(lista_salas):
    """Devolve um texto em forma de tabela com as salas informadas.

    Se a lista estiver vazia, devolve uma mensagem avisando que não há salas.
    """
    if not lista_salas:
        return "Não há salas disponíveis."

    # Cada sala vira uma linha de textos, na mesma ordem dos títulos
    linhas = [
        [str(s["id"]), s["nome"], str(s["capacidade"]), s["localizacao"]]
        for s in lista_salas
    ]

    larguras = _calcular_larguras(TITULOS_LISTAGEM, linhas)
    separador = "  ".join("-" * largura for largura in larguras)

    partes = [_montar_linha(TITULOS_LISTAGEM, larguras), separador]
    partes += [_montar_linha(linha, larguras) for linha in linhas]
    return "\n".join(partes)