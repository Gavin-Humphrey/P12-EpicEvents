from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from accounts.models import User, Client
from contracts.models import Contract
from events.models import Event
from rest_framework.exceptions import PermissionDenied 




class IsManagement(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user.is_superuser:
            return True


class IsSales(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        kwargs = view.kwargs

        if user.groups.filter(name="SALES").exists(): 
            print(user, view.action)           
            if view.action in ["list", "create"]:
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
            if "contracts" in request.path_info:
                if view.action == 'update' and obj.is_signed is True:
                    raise PermissionDenied("Cannot update a signed contract.")
            return True


class IsSupport(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if Group.objects.get(name='SUPPORT') in user.groups.all():
            if view.action == "list":
                return True
            elif view.kwargs.get('pk'):
                event = get_object_or_404(Event, pk=view.kwargs['pk'])
                if event.support_contact == user:
                    return True

    def has_object_permission(self, request, view, obj):

        support_team_events = ['update']
        if "events" in request.path_info and view.action in support_team_events:
            if obj.support_contact == request.user:
                return True
