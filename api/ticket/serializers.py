from rest_framework import serializers

from api.ticket.models import Ticket
from api.event.serializers import EventListSerializer


class TicketSerializer(serializers.ModelSerializer):
    event = EventListSerializer()

    class Meta:
        model = Ticket
        fields = ['event', 'row_number', 'seat_number']
