# language: pt
Funcionalidade: Edição e exclusão de salas
  Como responsável pelo sistema de reservas
  Quero alterar informações de salas e remover salas do sistema
  Para manter o cadastro de salas atualizado e consistente com as reservas

  Cenário: Editar informações de uma sala com sucesso
    Dado que existe uma sala cadastrada com nome "Sala 01", capacidade 20 e localização "Bloco A"
    Quando altero o nome para "Sala VIP", a capacidade para 25 e a localização para "Bloco B"
    Então os dados da sala devem ser atualizados com sucesso

  Cenário: Editar apenas a capacidade de uma sala
    Dado que existe uma sala cadastrada com nome "Sala 01", capacidade 20 e localização "Bloco A"
    Quando altero apenas a capacidade para 30
    Então a capacidade da sala deve ser 30 e os demais dados devem ser mantidos

  Cenário: Não permitir editar sala inexistente
    Dado que estou no sistema de gerenciamento de salas
    Quando tento editar uma sala com id inexistente 999
    Então a alteração deve ser recusada com a mensagem "Sala não encontrada."

  Cenário: Não permitir editar sala com nome vazio
    Dado que existe uma sala cadastrada com nome "Sala 01", capacidade 20 e localização "Bloco A"
    Quando altero o nome para ""
    Então a alteração deve ser recusada com a mensagem "O nome da sala é obrigatório."
    E os dados originais da sala devem ser mantidos

  Cenário: Não permitir editar sala com capacidade inválida
    Dado que existe uma sala cadastrada com nome "Sala 01", capacidade 20 e localização "Bloco A"
    Quando altero a capacidade para 0
    Então a alteração deve ser recusada com a mensagem "A capacidade deve ser um número inteiro maior que zero."
    E os dados originais da sala devem ser mantidos

  Cenário: Excluir sala sem reservas com sucesso
    Dado que existe uma sala cadastrada com nome "Sala 01", capacidade 20 e localização "Bloco A"
    Quando solicito a exclusão da sala
    Então a sala deve ser removida do sistema com sucesso

  Cenário: Excluir sala com reservas passadas com sucesso
    Dado que existe uma sala cadastrada com reservas apenas no passado
    Quando solicito a exclusão da sala
    Então a sala deve ser removida do sistema com sucesso

  Cenário: Não permitir excluir sala inexistente
    Dado que estou no sistema de gerenciamento de salas
    Quando solicito a exclusão de uma sala com id 999
    Então a exclusão deve ser recusada com a mensagem "Sala não encontrada."

  Cenário: Não permitir excluir sala com reservas futuras
    Dado que existe uma sala cadastrada com reservas futuras
    Quando solicito a exclusão da sala
    Então a exclusão deve ser recusada com a mensagem "Não é possível excluir a sala: existem reservas futuras associadas."
    E a sala deve permanecer cadastrada no sistema
