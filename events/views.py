from rest_framework.viewsets import ModelViewSet
from accounts.views import MultipleSerializerMixin
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from . import serializers
from events.models import Event
from events.filters import EventFilter  
from accounts.models import SALES, SUPPORT
from accounts.permissions import (
    IsManagement,
    IsSales,
    IsSupport
    )




class EventViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = serializers.EventListSerializer
    detail_serializer_class = serializers.EventDetailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter
    permission_classes = [IsAuthenticated, IsManagement | IsSupport | IsSales] 
    

    def get_queryset(self):
        user = self.request.user

        if self.action == "list" and user.team  == SUPPORT:
            queryset = Event.objects.filter(support_contact=self.request.user)
        elif self.action == 'list' and user.team == SALES:
            return Event.objects.filter(contract__sales_contact=self.request.user)
        else:
            queryset = Event.objects.all()

        return queryset    
