"""from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .serializers import ChangePasswordSerializer


class ChangePasswordView(generics.UpdateAPIView):
    http_method_names = ['put', 'options']
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user"""


from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .serializers import UserSignupSerializer
User = get_user_model()


class SignupViewset(APIView):

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user.team == 'SALES':
                group = Group.objects.get(name='SALES')
            elif user.team == 'SUPPORT':
                group = Group.objects.get(name='SUPPORT')
            else:
                group = Group.objects.get(name='MANAGEMENT')
            user.groups.add(group)
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
