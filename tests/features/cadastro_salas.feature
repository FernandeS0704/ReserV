# language: pt
Funcionalidade: Cadastro e listagem de salas
  Como responsável pelo sistema de reservas
  Quero cadastrar salas e consultar as salas cadastradas
  Para manter o controle das salas que podem ser reservadas

  Cenário: Cadastrar uma sala com sucesso
    Dado que estou no sistema de gerenciamento de salas
    Quando informo o nome "Sala 01", a capacidade 20 e a localização "Bloco A"
    Então a sala deve ser cadastrada com sucesso
    E a sala deve receber um identificador único

  Cenário: Cadastrar várias salas
    Dado que estou no sistema de gerenciamento de salas
    Quando informo o nome "Sala 01", a capacidade 20 e a localização "Bloco A"
    E informo o nome "Sala 02", a capacidade 30 e a localização "Bloco B"
    Então as duas salas devem estar cadastradas com identificadores diferentes

  Cenário: Não cadastrar sala com nome vazio
    Dado que estou no sistema de gerenciamento de salas
    Quando informo o nome "", a capacidade 20 e a localização "Bloco A"
    Então o cadastro deve ser recusado com a mensagem "O nome da sala é obrigatório."
    E nenhuma sala deve ser adicionada à lista

  Cenário: Não cadastrar sala com localização vazia
    Dado que estou no sistema de gerenciamento de salas
    Quando informo o nome "Sala 01", a capacidade 20 e a localização ""
    Então o cadastro deve ser recusado com a mensagem "A localização da sala é obrigatória."
    E nenhuma sala deve ser adicionada à lista

  Cenário: Não cadastrar sala com capacidade zero
    Dado que estou no sistema de gerenciamento de salas
    Quando informo o nome "Sala 01", a capacidade 0 e a localização "Bloco A"
    Então o cadastro deve ser recusado com a mensagem "A capacidade deve ser um número inteiro maior que zero."
    E nenhuma sala deve ser adicionada à lista

  Cenário: Não cadastrar sala com capacidade negativa
    Dado que estou no sistema de gerenciamento de salas
    Quando informo o nome "Sala 01", a capacidade -5 e a localização "Bloco A"
    Então o cadastro deve ser recusado com a mensagem "A capacidade deve ser um número inteiro maior que zero."
    E nenhuma sala deve ser adicionada à lista

  Cenário: Não cadastrar sala com capacidade que não é um número
    Dado que estou no sistema de gerenciamento de salas
    Quando informo o nome "Sala 01", a capacidade abc e a localização "Bloco A"
    Então o cadastro deve ser recusado com a mensagem "A capacidade deve ser um número inteiro maior que zero."
    E nenhuma sala deve ser adicionada à lista

  Cenário: Listar salas cadastradas
    Dado que existem salas cadastradas
    Quando solicito a listagem de salas
    Então o sistema deve apresentar todas as salas cadastradas
    E a listagem deve mostrar o identificador, o nome, a capacidade e a localização de cada sala

  Cenário: Listar salas quando não há nenhuma cadastrada
    Dado que não existem salas cadastradas
    Quando solicito a listagem de salas
    Então o sistema deve informar que não há salas disponíveis