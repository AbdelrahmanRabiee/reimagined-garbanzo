import datetime
from django.db import models


from api.choices import ReservationStatus
from api.ticket.models import Ticket


class Reservation(models.Model):
    RESERVATION_STATUS = (
        (ReservationStatus.PROCESSING, 'Processing'),
        (ReservationStatus.PAID, 'Paid'),
        (ReservationStatus.FAILED, 'Failed')
    )
    # many to many relationship because we might have FAILD reservations so many tickets with many reservations
    tickets = models.ManyToManyField(Ticket, related_name='reservations')
    date_created = models.DateTimeField(default=datetime.datetime.now)
    status = models.CharField(choices=RESERVATION_STATUS, max_length=64, default=ReservationStatus.PROCESSING)

    def __str__(self):
        return f'Reservation: {self.pk} status: {self.status}'

    @property
    def no_tickets(self):
        """get number of tickets for the current reservation"""
        return len(self.tickets.all())

    @property
    def total_price(self):
        """get total price of tickets for the current reservation"""
        return self.tickets.all().aggregate(models.Sum('price'))['price__sum']


