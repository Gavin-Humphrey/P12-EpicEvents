from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError, SerializerMethodField
from .models import Client


User = get_user_model()

class UserListSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'team']
        extra_kwargs = {'password': {'write_only': True}}


class UserDetailSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', "password", "first_name", "last_name", "email", "date_joined", "is_superuser", "team"]
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
       
        if value is not None and len(value) >= 8:
            return make_password(value)
        raise ValidationError('Password is empty or inssuficient')


class ClientListSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'email', 'sales_contact']


class ClientDetailSerializer(serializers.ModelSerializer):
    """
    Client serializer, with sales contact info added as read_only fields.
    """
    class Meta:
        model = Client
        fields = '__all__'
        read_only__fields = ('date_created', 'date_updated','sales_contact',  "id")