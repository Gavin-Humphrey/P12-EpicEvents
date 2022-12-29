from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Contract
from rest_framework import fields
from accounts.models import User




class ContractListSerializer(ModelSerializer):

    class Meta:
        model = Contract
        fields = ["id", "client", "sales_contact", "status"]


class ContractDetailSerializer(ModelSerializer):
    payment_due = fields.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'])
    class Meta:
        model = Contract
        fields = '__all__'
        #read_only_fields = ['status']

    def validate_sales_contact(self, value):
        """
        Check if user is from  "SALES" team.
        """
        if value:
            user_instance = User.objects.get(pk=value.id)
            if user_instance.team != "SALES":
                raise ValidationError(
                    "WARNING: To be assigned to this client, this personel must be from the 'SALES' team'.")
            return value