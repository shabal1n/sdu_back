from django.shortcuts import render
from django.contrib.auth.models import User, Group
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from sdu.main.models import *
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import viewsets, filters, generics
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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # permission_classes = [permissions.IsAuthenticated]
    search_fields = ['user__username', 'user__email', 'user__sdu_id']


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['title']

class CoursesViewSet(viewsets.ModelViewSet):
    queryset = Courses.objects.all()
    serializer_class = CoursesSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # permission_classes = [permissions.IsAuthenticated]
    search_fields = ['title', 'teacher']

class ProjectsViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # permission_classes = [permissions.IsAuthenticated]
    search_fields = ['title', 'course__title', 'priority__title']

class PrioritiesViewSet(viewsets.ModelViewSet):
    queryset = Priorities.objects.all()
    serializer_class = PrioritiesSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # permission_classes = [permissions.IsAuthenticated]
    search_fields = ['title']

class TasksViewSet(viewsets.ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # permission_classes = [permissions.IsAuthenticated]
    search_fields = ['title', 'project__title', 'assigned_to__user__username', 'priority__title', 'status__title']

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
