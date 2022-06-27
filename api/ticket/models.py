from django.db import models

from api.event.models import Event


class Ticket(models.Model):
    ticket_number = models.IntegerField()
    event = models.ForeignKey(Event, on_delete=models.PROTECT, related_name='tickets')
    row_number = models.IntegerField(null=True, blank=True)
    seat_number = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=10)

    def __str__(self):
        return f'ticket #{self.ticket_number} event: {self.event.title}'
