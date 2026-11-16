# language: pt
Funcionalidade: Busca de salas
  Como usuário do sistema de reservas
  Quero buscar salas por capacidade mínima e por localização
  Para encontrar rapidamente uma sala adequada ao meu evento

  Cenário: Buscar salas por capacidade mínima
    Dado a sala "Sala 01" cadastrada com capacidade 10 e localização "Bloco A"
    E a sala "Laboratório" cadastrada com capacidade 30 e localização "Bloco B"
    E a sala "Auditório" cadastrada com capacidade 100 e localização "Bloco B"
    Quando busco salas com capacidade mínima de 30
    Então as salas encontradas devem ser "Laboratório" e "Auditório"

  Cenário: Buscar salas por localização
    Dado a sala "Sala 01" cadastrada com capacidade 10 e localização "Bloco A"
    E a sala "Laboratório" cadastrada com capacidade 30 e localização "Bloco B"
    E a sala "Auditório" cadastrada com capacidade 100 e localização "Bloco B"
    Quando busco salas na localização "Bloco B"
    Então as salas encontradas devem ser "Laboratório" e "Auditório"

  Cenário: Combinar capacidade mínima e localização
    Dado a sala "Sala 01" cadastrada com capacidade 10 e localização "Bloco A"
    E a sala "Laboratório" cadastrada com capacidade 30 e localização "Bloco B"
    E a sala "Auditório" cadastrada com capacidade 100 e localização "Bloco B"
    Quando busco salas com capacidade mínima de 50 na localização "Bloco B"
    Então apenas a sala "Auditório" deve ser encontrada

  Cenário: Busca sem nenhuma sala que atenda aos critérios
    Dado a sala "Sala 01" cadastrada com capacidade 10 e localização "Bloco A"
    Quando busco salas com capacidade mínima de 50
    Então o sistema deve informar "Nenhuma sala encontrada para os critérios informados."

  Cenário: Recusar busca sem critérios
    Dado a sala "Sala 01" cadastrada com capacidade 10 e localização "Bloco A"
    Quando busco salas sem informar critérios
    Então a busca deve ser recusada com a mensagem "Informe ao menos um critério de busca: capacidade mínima ou localização."

  Cenário: Recusar capacidade mínima inválida
    Dado a sala "Sala 01" cadastrada com capacidade 10 e localização "Bloco A"
    Quando busco salas com capacidade mínima de 0
    Então a busca deve ser recusada com a mensagem "A capacidade mínima deve ser um número inteiro maior que zero."
