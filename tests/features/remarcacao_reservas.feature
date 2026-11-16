# language: pt
Funcionalidade: Remarcação de reservas
  Como usuário do sistema de reservas
  Quero remarcar uma reserva existente para outra data e horário
  Para ajustar o uso da sala sem precisar cancelar e reservar de novo

  Cenário: Remarcar reserva para um horário livre
    Dado que existe uma sala com uma reserva ativa na data "20/11/2026" e horário "10:00-11:00"
    Quando remarco essa reserva para a data "21/11/2026" e horário "14:00-15:00"
    Então a reserva deve estar na data "21/11/2026" e horário "14:00-15:00"

  Cenário: Remarcar libera o horário antigo da sala
    Dado que existe uma sala com uma reserva ativa na data "20/11/2026" e horário "10:00-11:00"
    Quando remarco essa reserva para a data "21/11/2026" e horário "14:00-15:00"
    Então a sala deve estar disponível na data "20/11/2026" e horário "10:00-11:00"

  Cenário: Recusar remarcação para horário ocupado
    Dado que existe uma sala com uma reserva ativa na data "20/11/2026" e horário "10:00-11:00"
    E a mesma sala tem outra reserva ativa na data "20/11/2026" e horário "14:00-15:00"
    Quando remarco essa reserva para a data "20/11/2026" e horário "14:00-15:00"
    Então a remarcação deve ser recusada com a mensagem "O horário já está reservado para esta sala."
    E a reserva deve estar na data "20/11/2026" e horário "10:00-11:00"

  Cenário: Recusar remarcação de reserva inexistente
    Dado que não existe uma reserva com id 99
    Quando tento remarcar a reserva 99 para a data "21/11/2026" e horário "14:00-15:00"
    Então a remarcação deve ser recusada com a mensagem "Reserva não encontrada."

  Cenário: Recusar remarcação de reserva cancelada
    Dado que existe uma reserva cancelada
    Quando remarco essa reserva para a data "21/11/2026" e horário "14:00-15:00"
    Então a remarcação deve ser recusada com a mensagem "Não é possível remarcar uma reserva cancelada."

  Cenário: Recusar remarcação sem data
    Dado que existe uma sala com uma reserva ativa na data "20/11/2026" e horário "10:00-11:00"
    Quando remarco essa reserva para a data "" e horário "14:00-15:00"
    Então a remarcação deve ser recusada com a mensagem "O campo data é obrigatório."

  Cenário: Recusar remarcação para a mesma data e horário
    Dado que existe uma sala com uma reserva ativa na data "20/11/2026" e horário "10:00-11:00"
    Quando remarco essa reserva para a data "20/11/2026" e horário "10:00-11:00"
    Então a remarcação deve ser recusada com a mensagem "A reserva já está nesta data e horário."
