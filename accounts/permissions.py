import logging

from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Group
from accounts.models import Client
from contracts.models import Contract
from events.models import Event
from django.core.exceptions import ObjectDoesNotExist, ValidationError


logger = logging.getLogger(__name__)


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
            elif kwargs.get("pk"):
                if "clients" in request.path_info:
                    try:
                        client = Client.objects.get(pk=kwargs.get("pk"))
                    except ObjectDoesNotExist as e:
                        self.message = e
                        logger.info(f"User access denied! {e}")
                        return False
                    if client.sales_contact in [request.user, None]:
                        return True     

                if "contracts" in request.path_info:
                    try:
                        contract = Contract.objects.get(pk=kwargs.get("pk"))
                    except ObjectDoesNotExist as e:
                        self.message = e
                        logger.info(f"User access denied! {e}")
                        return False    
                    if contract.sales_contact in [request.user, None]:
                        return True
                                                             

    def has_object_permission(self, request, view, obj):
        if obj.sales_contact in [request.user, None]:
            if "contracts" in request.path_info:
                if view.action == "update" and obj.is_signed is True:
                    logger.warning("Request denied! User tried to update a signed contract.")
                    return False
            return True



class IsSupport(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if Group.objects.get(name="SUPPORT") in user.groups.all():
            if view.action == "list":
                return True
            elif view.kwargs.get("pk"):
                try:
                    event = Event.objects.get(pk=view.kwargs["pk"])
                except ObjectDoesNotExist as e:
                    self.message = e
                    logger.warning(f"User access denied! {e}")
                    return False
                if event.support_contact == user:
                    return True

    def has_object_permission(self, request, view, obj):
        support_team_events = ["update", "retrieve"]
        if "events" in request.path_info and view.action in support_team_events:
            if obj.support_contact == request.user:
                return True
            else:
                logger.warning("User tried to alter an unauthorized event.")
                return False