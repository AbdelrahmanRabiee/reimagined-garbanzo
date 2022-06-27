from django.contrib import admin

from api.ticket.models import Ticket


class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'ticket_number', 'event', 'row_number', 'seat_number']


admin.site.register(Ticket, TicketAdmin)
