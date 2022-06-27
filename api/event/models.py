import datetime

from django.db import models

from api.choices import ReservationStatus, EventType

ACTIVE_STATUS = [ReservationStatus.PROCESSING, ReservationStatus.PAID]


class Event(models.Model):
    EVENT_TYPE = (
        (EventType.THEATRE, 'Theatre'),
        (EventType.CONCERT, 'Concert'),
        (EventType.CLUB, 'Club'),
        (EventType.STANDUP, 'Standup')
    )

    title = models.CharField(max_length=120)
    description = models.TextField(max_length=500, null=True, blank=True)
    event_type = models.CharField(choices=EVENT_TYPE, max_length=50, default=EventType.THEATRE)
    date = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.title

    def available_tickets(self):
        tickets = self.tickets.exclude(reservations__status__in=ACTIVE_STATUS)
        return tickets

    def unavailable_tickets(self):
        tickets = self.tickets.filter(reservations__status__in=ACTIVE_STATUS)
        return tickets

