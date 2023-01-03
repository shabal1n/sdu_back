from django.contrib.auth.models import User
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from sdu.main.models import *
from rest_framework import viewsets, filters, generics, authentication, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from sdu.main.serializers import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    search_fields = ['username', '=email']


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # authentication_classes = (JWTAuthentication)
    # permission_classes = [permissions.IsAuthenticated]
    # search_fields = ['user__username', 'user__email']

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user.id)


class ProjectsViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer
    


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
