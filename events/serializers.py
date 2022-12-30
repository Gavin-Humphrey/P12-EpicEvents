from rest_framework.serializers import ModelSerializer
from .models import Event



class EventListSerializer(ModelSerializer):

    class Meta:
        model = Event
        fields = ['id', 'name', 'location', 'event_status', 'client', 'support_contact']


class EventDetailSerializer(ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'
