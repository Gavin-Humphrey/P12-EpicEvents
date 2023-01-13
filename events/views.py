from rest_framework.viewsets import ModelViewSet
from accounts.views import MultipleSerializerMixin
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from . import serializers
from rest_framework.response import Response
from events.models import Event
from events.filters import EventFilter
from accounts.models import SUPPORT, SALES
from accounts.permissions import IsManagement, IsSales, IsSupport


class EventViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = serializers.EventListSerializer
    detail_serializer_class = serializers.EventDetailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter
    permission_classes = [IsAuthenticated, IsManagement | IsSupport | IsSales]
    

    def get_queryset(self):
        user = self.request.user

        if user.team == SUPPORT and not user.is_superuser:
            queryset = Event.objects.filter(support_contact=self.request.user).order_by(
                "id"
            )
        elif user.team == SALES and not user.is_superuser:
            queryset = Event.objects.filter(
                contract__sales_contact=self.request.user
            ).order_by("id")
        else:
            queryset = Event.objects.all().order_by("id")
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = serializers.EventListSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
