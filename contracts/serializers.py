from rest_framework import serializers
from .models import Contract
from rest_framework import fields



class ContractSerializer(serializers.ModelSerializer):
    #payment_due = fields.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'])
    class Meta:
        model = Contract
        fields = "__all__"
        read_only__fields = ('id', 'date_created', 'date_updated', 'sales_contact')