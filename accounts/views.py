from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .serializers import ChangePasswordSerializer


class ChangePasswordView(generics.UpdateAPIView):
    http_method_names = ['put', 'options']
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user
