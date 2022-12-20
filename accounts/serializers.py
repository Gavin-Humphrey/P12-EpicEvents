"""from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User




class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance
"""


from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer, ValidationError, SerializerMethodField
from rest_framework_simplejwt.tokens import RefreshToken


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
