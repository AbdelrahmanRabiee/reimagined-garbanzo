from django.contrib import admin

from api.event.models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'date']


admin.site.register(Event, EventAdmin)

