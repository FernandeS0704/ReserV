import pytest

from src import armazenamento


@pytest.fixture(autouse=True)
def limpar_armazenamento():
    armazenamento.reiniciar()
    yield
    armazenamento.reiniciar()