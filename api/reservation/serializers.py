from rest_framework import serializers

from api.reservation.models import Reservation
from api.ticket.serializers import TicketSerializer
from api.ticket.models import Ticket
from api.reservation import utils
from api.reservation.tasks import release_tickets


class ReservationCreateSerializer(serializers.ModelSerializer):
    tickets = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all(), many=True)

    class Meta:
        model = Reservation
        fields = ['tickets', ]

    def validate_tickets(self, tickets):
        # validate tickets list is not empty
        if not tickets:
            raise serializers.ValidationError({'error_message': 'Ticket numbers must be provided'})

        # based on the business logic you should add or combine different validators
        validators = [utils.UnavailableTicketsValidation]
        if tickets[0].row_number is None:
            validators += [
                utils.EvenValidation,
                utils.AvoidOneValidation,
                utils.AllTogetherValidation
            ]
        else:
            validators += [
                utils.EvenValidationWithRowNumber,
                utils.AvoidOneValidationWithRowNumber,
                utils.AllTogetherValidationWithRowNumber
            ]

        reservation = utils.ReservationValidationService()

        # apply the validators on the selected tickets
        for validator in validators:
            reservation.selling_option = validator()
            result = reservation.validate(tickets)
            if result is not True:
                raise serializers.ValidationError({'error_message': result})
        return tickets

    def create(self, validated_data):
        """override create method to call celery task that release tickets after 15 minutes"""
        reservation = Reservation.objects.create()
        for ticket in validated_data.get('tickets'):
            reservation.tickets.add(ticket)

        # after 15 minutes release tickets and change reservation status to FAILD if status is not PAID
        release_tickets.apply_async(args=[reservation.id, ], countdown=15*60)
        return reservation


class ReservationListSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True)

    class Meta:
        model = Reservation
        fields = ['id', 'tickets', 'no_tickets', 'total_price', 'date_created', 'status']
