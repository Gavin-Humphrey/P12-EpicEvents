from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError, SerializerMethodField
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Client


User = get_user_model()


class UserSignupSerializer(ModelSerializer):

    tokens = SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'password',
            'first_name',
            'last_name',
            'mobile',
            'team',
            'tokens'
        ]

    def validate_email(self, value: str) -> str:
        if User.objects.filter(email=value).exists():
            raise ValidationError('User already exists')
        return value

    def validate_password(self, value: str) -> str:
        if value is not None:
            return make_password(value)
        raise ValidationError('Password is empty')

    def get_tokens(self, user: User) -> dict:
        tokens = RefreshToken.for_user(user)
        data = {
            'refresh': str(tokens),
            'access': str(tokens.access_token)
        }
        return data


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'phone',
            'team',
        ]



class ClientSerializer(serializers.ModelSerializer):
    """
    Client serializer, with sales contact info added as read_only fields.
    """
    sales_contact_first_name = serializers.CharField(read_only=True, source='sales_contact.first_name')
    sales_contact_last_name = serializers.CharField(read_only=True, source='sales_contact.last_name')
    sales_contact_email = serializers.CharField(read_only=True, source='sales_contact.email')

    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'mobile', 'date_created', 'date_updated',
                  'company_name', 'sales_contact', 'sales_contact_first_name', 'sales_contact_last_name',
                  'sales_contact_email']
