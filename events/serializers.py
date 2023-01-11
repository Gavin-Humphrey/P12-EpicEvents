from rest_framework.serializers import ModelSerializer
from .models import Event


class EventListSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "contract",
            "name",
            "location",
            "event_status",
            "support_contact",
            "event_date",
        ]


class EventDetailSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
