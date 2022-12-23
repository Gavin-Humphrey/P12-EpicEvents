from rest_framework.permissions import BasePermission
from accounts.models import User, Client
from contracts.models import Contract


class IsManagement(BasePermission):
    def has_permission(self, request, view):
        if request.user and bool(request.user.groups.filter(name='MANAGEMENT')):
            print('Management confirmed!')
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return True


class IsSales(BasePermission):
    message = "You don't have permission to do that. Need to be Sales or Management"

    def has_permission(self, request, view):
        if request.user and bool(request.user.groups.filter(name='SALES')):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if type(obj) == Contract or type(obj) == Client:
            if view.action in ['update', 'partial_update', 'retrieve', 'list']:
                return True
            if view.action == 'destroy':
                return False


class IsSupport(BasePermission):
    message = "You don't have permission to do that. Need to be Support or Management"

    def has_permission(self, request, view):
        if request.user and bool(request.user.groups.filter(name='SUPPORT')):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if type(obj) == Contract or type(obj) == Client:
            if view.action in ['retrieve', 'list']:
                return True
            if view.action in ['update', 'partial_update', 'destroy']:
                return False
        