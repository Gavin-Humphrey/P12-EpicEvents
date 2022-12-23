from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from accounts.filters import ClientFilter
from .models import Client
from .serializers import ClientSerializer
from .permissions import IsSales, IsSupport, IsManagement


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



class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ClientFilter

    def get_permissions(self):
        """
        Overload of get_permission method of parent class ModelViewSet.
        Defines permission_classes depending on the action.
        - List or retrieve for authenticated users.
        :return: A list of permissions.
        """
        permission_classes = [permissions.IsAuthenticated(),]
        if self.action == 'retrieve' or self.action == 'list':
            permission_classes = [permissions.IsAuthenticated(),IsManagement | IsSales | IsSupport,]
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated(),IsManagement | IsSales,]
        if self.action == 'update' or self.action == 'partial_update':
            permission_classes = [permissions.IsAuthenticated(), IsManagement | IsSales,]
        if self.action == 'destroy':
            permission_classes = [permissions.IsAuthenticated(), IsManagement,]
        return permission_classes