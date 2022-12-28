from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from accounts.models import User, Client
from contracts.models import Contract



"""class IsManagement(BasePermission):
    def has_permission(self, request, view):
        if request.user and bool(request.user.groups.filter(name='MANAGEMENT')):
            print('Management confirmed')
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return True"""


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if user.is_superuser:
            return True


class IsSales(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        kwargs = view.kwargs

        if user.groups.filter(name="SALES").exists():            
            if view.action in ["list", "create", "signed"]:
                return True
            elif view.action == "destroy":
                return False
            elif kwargs.get('pk'): 
                if "clients" in request.path_info:
                    client = get_object_or_404(Client, pk=kwargs.get('pk'))
                    if client.sales_contact in [request.user, None]:
                        return True
                if "contracts" in request.path_info:
                    contract = get_object_or_404(Contract, pk=kwargs.get('pk'))
                    if contract.sales_contact in [request.user, None]:
                        return True        
                    

    def has_object_permission(self, request, view, obj):

        if obj.sales_contact in [request.user, None]:
            return True


