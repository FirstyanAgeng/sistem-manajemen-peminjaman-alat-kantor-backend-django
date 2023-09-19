from rest_framework import generics, authentication, permissions 
from user.serializers import UserSerializer 
from rest_framework.authtoken.views import ObtainAuthToken 
from user.serializers import (AuthTokenSerializer, UserSerializer)
from rest_framework.settings import api_settings 
from rest_framework import viewsets
from core.models import User

# membuat user
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer 

# membuat token 
class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer 
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

# kelola user 
class ManageUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer 
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user