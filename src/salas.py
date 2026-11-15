from datetime import date, datetime

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


def buscar_sala_por_id(id_sala):
    for sala in armazenamento.salas:
        if sala["id"] == id_sala:
            return sala
    raise ValueError("Sala não encontrada.")


def editar_sala(id_sala, nome=None, capacidade=None, localizacao=None):
    sala = buscar_sala_por_id(id_sala)

    if nome is not None and not _texto_preenchido(nome):
        raise ValueError("O nome da sala é obrigatório.")

    if localizacao is not None and not _texto_preenchido(localizacao):
        raise ValueError("A localização da sala é obrigatória.")

    if capacidade is not None and not _capacidade_valida(capacidade):
        raise ValueError("A capacidade deve ser um número inteiro maior que zero.")

    if nome is not None:
        sala["nome"] = nome
    if capacidade is not None:
        sala["capacidade"] = capacidade
    if localizacao is not None:
        sala["localizacao"] = localizacao

    return sala


def _converter_data(valor):
    if isinstance(valor, datetime):
        return valor
    if isinstance(valor, date):
        return datetime.combine(valor, datetime.min.time())
    if isinstance(valor, str):
        try:
            return datetime.fromisoformat(valor)
        except ValueError:
            try:
                data = datetime.strptime(valor, "%d/%m/%Y")
            except ValueError:
                return None
            return data.replace(hour=23, minute=59, second=59, microsecond=999999)
    return None


def _tem_reservas_futuras(id_sala, agora=None):
    if agora is None:
        agora = datetime.now()
    for reserva in getattr(armazenamento, "reservas", []):
        if reserva.get("status") == "cancelada":
            continue
        if reserva.get("sala_id") == id_sala:
            fim = reserva.get("data_fim") or reserva.get("data") or reserva.get("data_inicio")
            data_dt = _converter_data(fim)
            if data_dt and data_dt >= agora:
                return True
    return False


def excluir_sala(id_sala):
    sala = buscar_sala_por_id(id_sala)
    if _tem_reservas_futuras(id_sala):
        raise ValueError("Não é possível excluir a sala: existem reservas futuras associadas.")
    armazenamento.salas.remove(sala)
    return True


def listar_salas():
    return list(armazenamento.salas)

TITULOS_LISTAGEM = ["ID", "Nome", "Capacidade", "Localização"]


def _calcular_larguras(titulos, linhas):

    larguras = []
    for i, titulo in enumerate(titulos):
        valores = [len(linha[i]) for linha in linhas]
        larguras.append(max([len(titulo)] + valores))
    return larguras


def _montar_linha(colunas, larguras):
    return "  ".join(
        coluna.ljust(largura) for coluna, largura in zip(colunas, larguras)
    ).rstrip()


def formatar_listagem(lista_salas):
    if not lista_salas:
        return "Não há salas disponíveis."

    linhas = [
        [str(s["id"]), s["nome"], str(s["capacidade"]), s["localizacao"]]
        for s in lista_salas
    ]

    larguras = _calcular_larguras(TITULOS_LISTAGEM, linhas)
    separador = "  ".join("-" * largura for largura in larguras)

    partes = [_montar_linha(TITULOS_LISTAGEM, larguras), separador]
    partes += [_montar_linha(linha, larguras) for linha in linhas]
    return "\n".join(partes)
