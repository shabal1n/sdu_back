from django.contrib.auth.models import User
from django.urls import reverse
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from sdu.main.models import *
from rest_framework import (
    viewsets,
    filters,
    generics,
    generics,
    viewsets,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from sdu.main.serializers import *
from rest_framework.response import Response
from rest_framework import generics


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    search_fields = ["username", "=email"]


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

    @action(detail=False, methods=["GET"], name="Get My Projects")
    def my(self, request):
        profile = Profile.objects.get(user=self.request.user.id)
        projects = Projects.objects.filter(participants=profile.id)
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)


class TasksViewSet(viewsets.ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer

    def get_queryset(self):
        return Tasks.objects.filter(project=self.request.data["project_id"])

    @action(detail=False, methods=["GET"], name="Get My Tasks")
    def my(self, request):
        profile = Profile.objects.get(user=self.request.user.id)
        tasks = Tasks.objects.filter(project__participants=profile.id)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"], name="Get Task Details")
    def details(self, request):
        task = Tasks.objects.get(id=self.request.data["task_id"])
        serializer = TasksDetailSerializer(task)
        return Response(serializer.data)

    @action(detail=False, methods=["POST"], name="Edit Task Data")
    def edit(self, request):
        task = Tasks.objects.get(id=self.request.data["task_id"])
        task.assigned_to.add(Profile.objects.get(id=self.request.data["assigned_to"]))
        task.title = self.request.data["title"]
        task.deadline = self.request.data["deadline"]
        task.description = self.request.data["description"]
        task.status = TaskStatuses.objects.get(id=self.request.data["status"])
        task.save()
        return Response("Task edited")

    @action(detail=False, methods=["DELETE"], name="Delete Task")
    def delete(self, request):
        task = Tasks.objects.get(id=self.request.data["task_id"])
        task.delete()
        return Response("Task deleted")


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = RegisterSerializer


class DashboardView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = DashboardSerializer

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user.id)


class ProfilePageView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfilePageSerializer

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user.id)

    @action(detail=False, methods=["POST"], name="Change Status")
    def change_status(self, request):
        profile = Profile.objects.get(user=self.request.user.id)
        profile.status = UserStatuses.objects.get(id=self.request.data["status"])
        profile.save()
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    @action(detail=False, methods=["POST"], name="Edit Profile Data")
    def edit_profile(self, request):
        profile = Profile.objects.get(user=self.request.user.id)
        profile.year_of_study = self.request.data["year_of_study"]
        profile.birth_date = self.request.data["birth_date"]
        profile.language = self.request.data["language"]
        profile.course_of_study = self.request.data["course_of_study"]
        profile.picture_url = self.request.data["picture_url"]
        profile.save()
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


class AnalyticsPageViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = AnalyticsSerializer

    def get(self, request, format=None):
        profile = Profile.objects.filter(user=self.request.user.id)
        projects = Projects.objects.filter(participants=profile[0].id)
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"], name="Get Analytics Data")
    def extended(self, request):
        profile = Profile.objects.filter(user=self.request.user.id)
        projects = Projects.objects.filter(participants=profile[0].id)
        serializer = AnalyticsExtendedSerializer(
            projects, context={"request": request}, many=True
        )
        return Response(serializer.data)
    
class CoursesViewSet(viewsets.ModelViewSet):
    queryset = Courses.objects.all()
    serializer_class = CoursesSerializer

    def get(self, request):
        profile = Profile.objects.get(user=self.request.user.id)
        if profile.is_supervisor:
            courses = Courses.objects.filter(course_supervisor=profile)
        serializer = CoursesSerializer(courses, many=True)
        return Response(serializer.data)