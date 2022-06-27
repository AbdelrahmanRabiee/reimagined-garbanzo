from abc import ABC, abstractmethod


class ValidationInterface(ABC):
    @abstractmethod
    def validate(self, tickets):
        pass

    @abstractmethod
    def error_message(self):
        pass

    def handle_tickets(self, tickets):
        """handle tickets if it cares for row_number or quantity"""
        if tickets[0].row_number is not None:
            return self._handle_tickets_with_row(tickets)
        else:
            return tickets

    def _handle_tickets_with_row(self, tickets):
        row_tickets = {}
        for ticket in tickets:
            if ticket.row_number in row_tickets:
                row = row_tickets[ticket.row_number]
                row.append(ticket)
                row_tickets[ticket.row_number] = row
            else:
                row_tickets[ticket.row_number] = list([ticket, ])
        return row_tickets


class EvenValidation(ValidationInterface):
    def validate(self, tickets_list):
        tickets_list = self.handle_tickets(tickets_list)
        valid = True
        if len(tickets_list) % 2 != 0:
            valid = False
        return valid

    def error_message(self):
        return 'Number of tickets must be even'


class EvenValidationWithRowNumber(EvenValidation):
    def validate(self, tickets_list):
        tickets_list = self.handle_tickets(tickets_list)
        valid = True
        for row, tickets in tickets_list.items():
            if len(tickets) % 2 != 0:
                valid = False
                return valid

        return valid


class AvoidOneValidation(ValidationInterface):
    def validate(self, tickets_list):
        tickets = self.handle_tickets(tickets_list)
        ticket_ids = [ticket.id for ticket in tickets]
        event = tickets[0].event
        available_tickets_num = event.available_tickets().exclude(
                id__in=ticket_ids).count()
        valid = available_tickets_num != 1

        return valid

    def error_message(self):
        return 'There is a one ticket left and this is not allowed, you should reserve it'


class AvoidOneValidationWithRowNumber(AvoidOneValidation):
    def validate(self, tickets_list):
        tickets_list = self.handle_tickets(tickets_list)
        valid = True
        for row, tickets in tickets_list.items():
            ticket_ids = [ticket.id for ticket in tickets]
            event = tickets[0].event
            available_tickets_num = event.available_tickets().filter(row_number=row).exclude(
                    id__in=ticket_ids).count()
            valid = available_tickets_num != 1

            if not valid:
                return valid

        return valid


class AllTogetherValidation(ValidationInterface):
    def validate(self, tickets_list):
        tickets = self.handle_tickets(tickets_list)
        valid = True
        seat_numbers = [ticket.seat_number for ticket in tickets]
        sorted_seat_numbers = list(sorted(seat_numbers))

        current_seat = sorted_seat_numbers[0]
        for seat in sorted_seat_numbers:
            valid = valid and current_seat == seat
            current_seat += 1
            if not valid:
                return valid
        return valid

    def error_message(self):
        return 'There is a gap between seats numbers and this is not allowed'


class AllTogetherValidationWithRowNumber(AllTogetherValidation):
    def validate(self, tickets_list):
        tickets_list = self.handle_tickets(tickets_list)
        valid = True
        for row, tickets in tickets_list.items():
            seat_numbers = [ticket.seat_number for ticket in tickets]
            sorted_seat_numbers = list(sorted(seat_numbers))

            current_seat = sorted_seat_numbers[0]
            for seat in sorted_seat_numbers:
                valid = valid and current_seat == seat
                current_seat += 1
                if not valid:
                    return valid
        return valid


class UnavailableTicketsValidation(ValidationInterface):
    def validate(self, tickets):
        ticket_ids = [ticket.id for ticket in tickets]
        event = tickets[0].event
        unavailable_tickets = event.unavailable_tickets().filter(id__in=ticket_ids).count()
        valid = unavailable_tickets == 0

        return valid

    def error_message(self):
        return 'some tickets are unavailable'


class ReservationValidationService:
    def __init__(self):
        self._validation_selling_option = None

    @property
    def selling_option(self):
        return self._validation_selling_option

    @selling_option.setter
    def selling_option(self, option):
        self._validation_selling_option = option

    def validate(self, tickets):
        if self._validation_selling_option.validate(tickets):
            return True
        return self._validation_selling_option.error_message()




