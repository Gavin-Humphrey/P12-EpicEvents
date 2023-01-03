from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Contract
from rest_framework import fields
from accounts.models import User, Client




class ContractListSerializer(ModelSerializer):
    

    class Meta:
        model = Contract
        fields = ["id", "client", "sales_contact", "is_signed"]



class ContractDetailSerializer(ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'

        
    def validate_sales(self, data):
        """
        Check if client is linked to another personel in "SALES" team.
        """
        if data.get('client'):
            client = data['client']
            user = data['sales_contact']
            if client.sales_contact not in [user, None]:
                raise ValidationError("Cannot create a contract for a client linked to another sales personnel.")            
        return data

    