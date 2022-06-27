from rest_framework import serializers

from api.event.models import Event


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title']
