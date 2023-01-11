import logging
from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Contract

# from rest_framework import fields
from accounts.models import User, Client

logger = logging.getLogger(__name__)


class ContractListSerializer(ModelSerializer):
    class Meta:
        model = Contract
        fields = ["id", "client", "sales_contact", "is_signed", "amount"]
        read_only__fields = ["id", "date_created", "date_updated", "sales_contact"]


class ContractDetailSerializer(ModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"

    def validate(self, data):
        """Validate contract if sales_contact is the sales_contact of the client"""

        sales_contact: User = data["sales_contact"]
        client: Client = data["client"]
        if client.sales_contact != sales_contact:
            raise ValidationError(
                "User cannot create a contract for a client linked to another sales personnel."
            )
        return data
