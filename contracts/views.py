from rest_framework import status, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, action
from .models import Contract
from .filters import ContractFilter
from . import serializers
from accounts.views import MultipleSerializerMixin
from accounts.models import User, Client, SALES, SUPPORT
from events.serializers import EventDetailSerializer
from accounts.permissions import (IsManagement, IsSales, IsSupport,)

from django.core.exceptions import ValidationError

from .serializers import *




class ContractViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = serializers.ContractListSerializer
    detail_serializer_class = serializers.ContractDetailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContractFilter
    permission_classes = [IsAuthenticated, IsManagement | IsSales | IsSupport] 
   

    def get_queryset(self):
        user = self.request.user

        if self.action == 'list' and user.team == SALES and not user.is_superuser:
            queryset = Contract.objects.filter(sales_contact=self.request.user).order_by('id')
        if self.action == 'list' and user.team == SUPPORT and not user.is_superuser:
            queryset = Contract.objects.filter(event__support_contact=self.request.user).order_by('id')
        else:
            queryset = Contract.objects.all().order_by('id')

        return queryset
    
    #To do: make sure the sales_contact is same as client sales_contact
    def create(self, request):        
        data = request.data.copy()
        data['sales_contact'] = request.user.id

        serialized_data = self.detail_serializer_class(data=data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()
        client = Client.objects.get(pk=serialized_data.data.get('client'))
        if client.sales_contact is None:
            client.sales_contact = request.user
            client.save()  
        return Response(serialized_data.data, status=status.HTTP_202_ACCEPTED)


    def partial_update(self, request, contract_pk, obj):
        contract = Contract.objects.get(pk=contract_pk)
        serialized_data = self.detail_serializer_class(contract, data=request.data, partial=True)
       
        if serialized_data.is_valid(raise_exception=True):
            serialized_data.save()
            return Response(serialized_data.data, status=status.HTTP_202_ACCEPTED)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
        
