from django.contrib.auth.models import User
from django.urls import reverse
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from sdu.main.models import *
from rest_framework import viewsets, filters, generics, authentication, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from sdu.main.serializers import *
from rest_framework.response import Response


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
    
    @action(detail=False, methods=['GET'], name='Get My Projects')
    def my(self, request):
        profile = Profile.objects.get(user=self.request.user.id)
        projects = Projects.objects.filter(participants=profile.id)
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)

class TasksViewSet(viewsets.ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer

    def get_queryset(self): #TODO: fix this
        return Tasks.objects.filter(project=self.kwargs['project_pk'])

    @action(detail=False, methods=['GET'], name='Get My Tasks')
    def my(self, request):
        profile = Profile.objects.get(user=self.request.user.id)
        tasks = Tasks.objects.filter(project__participants=profile.id)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
