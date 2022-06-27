from django.contrib import admin

from api.reservation.models import Reservation


class ReservationAdmin(admin.ModelAdmin):
    list_display = ['id', 'date_created', 'status']


admin.site.register(Reservation, ReservationAdmin)
