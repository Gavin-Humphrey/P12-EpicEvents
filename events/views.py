from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from accounts.views import MultipleSerializerMixin
from django_filters.rest_framework import DjangoFilterBackend
from . import serializers
from events.models import Event
from accounts.permissions import (
    IsManagement,
    IsSales,
    IsSupport
    )




class EventViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = serializers.EventListSerializer
    detail_serializer_class = serializers.EventDetailSerializer
    permission_classes = [IsManagement | IsSupport]
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        user = self.request.user

        if self.action == "list" and not user.is_superuser:
            queryset = Event.objects.filter(support_contact=self.request.user)
        else:
            queryset = Event.objects.all()

        return queryset
