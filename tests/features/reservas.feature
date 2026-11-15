# language: pt
Funcionalidade: Gerenciamento de reservas de salas
  Como usuário do sistema
  Quero realizar e cancelar reservas
  Para organizar o uso das salas

  Cenário: Realizar uma reserva com sucesso
    Dado que existe uma sala disponível
    Quando realizo uma reserva para "Djames" na data "15/11/2026" e horário "19:00-20:00"
    Então a reserva deve ser criada com status "ativa"

  Cenário: Recusar reserva de sala inexistente
    Dado que não existe uma sala com id 99
    Quando tento reservar a sala 99 para "Djames" na data "15/11/2026" e horário "19:00-20:00"
    Então a reserva deve ser recusada com a mensagem "Sala não encontrada."

  Cenário: Impedir conflito de horário
    Dado que existe uma sala com uma reserva ativa na data "15/11/2026" e horário "19:00-20:00"
    Quando tento reservar a mesma sala para "Outra pessoa" na data "15/11/2026" e horário "19:00-20:00"
    Então a reserva deve ser recusada com a mensagem "O horário já está reservado para esta sala."

  Cenário: Cancelar uma reserva existente
    Dado que existe uma reserva ativa
    Quando cancelo essa reserva
    Então o status da reserva deve ser "cancelada"

  Cenário: Recusar cancelamento de reserva inexistente
    Dado que não existe uma reserva com id 99
    Quando tento cancelar a reserva 99
    Então o cancelamento deve ser recusado com a mensagem "Reserva não encontrada."

  Cenário: Recusar cancelamento repetido
    Dado que existe uma reserva já cancelada
    Quando tento cancelar essa reserva novamente
    Então o cancelamento deve ser recusado com a mensagem "A reserva já está cancelada."
