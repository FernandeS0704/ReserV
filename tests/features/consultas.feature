# language: pt
Funcionalidade: Consulta de disponibilidade e listagem de reservas
  Como usuário do sistema de reservas
  Quero consultar quais salas estão livres e ver as reservas realizadas
  Para escolher uma sala disponível e acompanhar o uso das salas

  Cenário: Consultar disponibilidade sem reservas no horário
    Dado que existem as salas "Sala 01" e "Sala 02" cadastradas
    Quando consulto a disponibilidade na data "20/11/2026" e horário "19:00-20:00"
    Então as salas disponíveis devem ser "Sala 01" e "Sala 02"

  Cenário: Sala reservada não aparece como disponível
    Dado que existem as salas "Sala 01" e "Sala 02" cadastradas
    E a sala "Sala 01" está reservada na data "20/11/2026" e horário "19:00-20:00"
    Quando consulto a disponibilidade na data "20/11/2026" e horário "19:00-20:00"
    Então apenas a sala "Sala 02" deve estar disponível

  Cenário: Sala reservada em outro horário continua disponível
    Dado que existem as salas "Sala 01" e "Sala 02" cadastradas
    E a sala "Sala 01" está reservada na data "20/11/2026" e horário "19:00-20:00"
    Quando consulto a disponibilidade na data "20/11/2026" e horário "20:00-21:00"
    Então as salas disponíveis devem ser "Sala 01" e "Sala 02"

  Cenário: Reserva cancelada libera a sala
    Dado que existem as salas "Sala 01" e "Sala 02" cadastradas
    E a sala "Sala 01" teve uma reserva cancelada na data "20/11/2026" e horário "19:00-20:00"
    Quando consulto a disponibilidade na data "20/11/2026" e horário "19:00-20:00"
    Então as salas disponíveis devem ser "Sala 01" e "Sala 02"

  Cenário: Nenhuma sala disponível no horário
    Dado que existem as salas "Sala 01" e "Sala 02" cadastradas
    E a sala "Sala 01" está reservada na data "20/11/2026" e horário "19:00-20:00"
    E a sala "Sala 02" está reservada na data "20/11/2026" e horário "19:00-20:00"
    Quando consulto a disponibilidade na data "20/11/2026" e horário "19:00-20:00"
    Então o sistema deve informar "Não há salas disponíveis."

  Cenário: Recusar consulta sem data
    Dado que existem as salas "Sala 01" e "Sala 02" cadastradas
    Quando consulto a disponibilidade na data "" e horário "19:00-20:00"
    Então a consulta deve ser recusada com a mensagem "O campo data é obrigatório."

  Cenário: Recusar consulta sem horário
    Dado que existem as salas "Sala 01" e "Sala 02" cadastradas
    Quando consulto a disponibilidade na data "20/11/2026" e horário ""
    Então a consulta deve ser recusada com a mensagem "O campo horário é obrigatório."

  Cenário: Listar reservas realizadas
    Dado que existem as salas "Sala 01" e "Sala 02" cadastradas
    E a sala "Sala 01" está reservada na data "20/11/2026" e horário "19:00-20:00"
    E a sala "Sala 02" está reservada na data "21/11/2026" e horário "08:00-10:00"
    Quando solicito a listagem de reservas
    Então o sistema deve apresentar 2 reservas
    E a listagem deve mostrar a sala, a data e o horário de cada reserva

  Cenário: Listar reserva cancelada com seu status
    Dado que existem as salas "Sala 01" e "Sala 02" cadastradas
    E a sala "Sala 01" teve uma reserva cancelada na data "20/11/2026" e horário "19:00-20:00"
    Quando solicito a listagem de reservas
    Então a reserva deve aparecer com o status "cancelada"

  Cenário: Listar reservas quando não há nenhuma realizada
    Dado que não existem reservas realizadas
    Quando solicito a listagem de reservas
    Então o sistema deve informar "Não há reservas realizadas."
