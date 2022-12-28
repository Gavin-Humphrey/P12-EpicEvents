from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, permission_classes
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib.auth.models import Group
from .permissions import IsAdmin, IsSales
from . import serializers
from accounts.filters import ClientFilter
from .models import Client


User = get_user_model()


class MultipleSerializerMixin:
    """Mixin for list and detail serializer."""

    detail_serializer_class = None

    def get_serializer_class(self):
        detail_serializer_actions = ['retrieve', 'update', 'partial_update', 'create']
        if self.action in detail_serializer_actions and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class UserViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = serializers.UserListSerializer
    detail_serializer_class = serializers.UserDetailSerializer
    permission_classes = (IsAdmin,)

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset


class ClientViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = serializers.ClientListSerializer
    detail_serializer_class = serializers.ClientDetailSerializer
    permission_classes = [IsAdmin|IsSales] #|IsSupport
    filterset_class = ClientFilter

    def get_queryset(self):
        user = self.request.user

        if self.action == "list" and not user.is_superuser:
            if Group.objects.get(name='SALES') in user.groups.all():
                queryset = Client.objects.filter(Q(sales_contact=user) | Q(sales_contact__isnull=True))
            elif Group.objects.get(name='SUPPORT') in user.groups.all():
                queryset = Client.objects.filter(events__support_contact=user)
            else:
                raise PermissionDenied("You currently are not in any of the authorized teams; contact the admin... ")
        else:
            queryset = Client.objects.all()
        return queryset


