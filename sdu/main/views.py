from django.shortcuts import render
from django.contrib.auth.models import User, Group
from sdu.main.models import *
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import viewsets, filters, generics
from django_filters.rest_framework import DjangoFilterBackend


from sdu.main.serializers import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    search_filter = ['username', 'email', 'password']


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

