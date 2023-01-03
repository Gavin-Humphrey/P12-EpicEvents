from rest_framework import status, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import permission_classes, action
from .models import Contract
from .filters import ContractFilter
from . import serializers
from accounts.views import MultipleSerializerMixin
from accounts.models import User, Client
from events.serializers import EventDetailSerializer
from accounts.permissions import (IsManagement, IsSales, IsSupport,)




class ContractViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = serializers.ContractListSerializer
    detail_serializer_class = serializers.ContractDetailSerializer
    filterset_class = ContractFilter
    permission_classes = [IsManagement | IsSales,] 
   

    def get_queryset(self):
        user = self.request.user

        if self.action == "list" and not user.is_superuser:
            queryset = Contract.objects.filter(sales_contact=self.request.user)
        else:
            queryset = Contract.objects.all()

        return queryset

    
    def create(self, request):        
        data = request.data.copy()
        data['sales_contact'] = request.user.id
        #data['is_signed'] = 'false'

        serialized_data = self.detail_serializer_class(data=data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()
        client = get_object_or_404(Client, pk=serialized_data.data.get('client'))
        if client.sales_contact is None:
            client.sales_contact = request.user
            client.save()
        return Response(serialized_data.data, status=status.HTTP_202_ACCEPTED)

##### Review the update and signing
    def partial_update(self, request, contract_pk, obj):
        contract = get_object_or_404(Contract, pk=contract_pk)
        serialized_data = self.detail_serializer_class(contract, data=request.data, partial=True)
       
        if serialized_data.is_valid(raise_exception=True):
            serialized_data.save()
            return Response(serialized_data.data, status=status.HTTP_202_ACCEPTED)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
        
