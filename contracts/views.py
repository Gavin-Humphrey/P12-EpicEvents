from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from .models import Contract
from .filters import ContractFilter
from .serializers import ContractSerializer
from .permissions import ContractPermissions
from accounts.permissions import (IsManagement, IsSales, IsSupport)



class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContractFilter


    def get_permissions(self):
        
        permission_classes = [permissions.IsAuthenticated(),]
        if self.action == 'retrieve' or self.action == 'list':
            permission_classes = [permissions.IsAuthenticated(), IsManagement | IsSales | IsSupport,]
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated(), IsManagement | IsSales,]
        if self.action == 'update' or self.action == 'partial_update':
            permission_classes = [permissions.IsAuthenticated(), IsManagement | IsSales,]
        if self.action == 'destroy':
            permission_classes = [permissions.IsAuthenticated(), IsManagement | ContractPermissions,]
        return permission_classes
