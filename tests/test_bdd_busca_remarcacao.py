# Testes BDD das funcionalidades de busca de salas e remarcação de reservas.
from pytest_bdd import scenarios

# Transforma cada cenário dos arquivos .feature em um teste do pytest.
scenarios("features/busca_salas.feature")
scenarios("features/remarcacao_reservas.feature")
