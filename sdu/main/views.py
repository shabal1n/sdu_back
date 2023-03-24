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
from django.http import HttpResponse
import json
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

    @action(detail=False, methods=["GET"], name="Get Project Details")
    def details(self, request):
        project = Projects.objects.get(id=request.GET["project_id"])
        tasks = Tasks.objects.filter(project=project.id)
        serializer = TasksDetailSerializer(tasks, many=True)
        result_dict = {}
        result_dict["project"] = project.title
        result_dict["to_do"] = list()
        result_dict["in_progress"] = list()
        result_dict["done"] = list()
        for i in serializer.data:
            if i["status"] == 1:
                result_dict["to_do"].append(i)
            elif i["status"] == 2:
                result_dict["in_progress"].append(i)
            elif i["status"] == 3:
                result_dict["done"].append(i)
        return Response(result_dict)


class TasksViewSet(viewsets.ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer

    def get_queryset(self):
        return Tasks.objects.filter(project=self.request.data["project_id"])
    
    def create(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user.id)
        project = Projects.objects.get(id=self.request.data["project"])

        if profile.is_supervisor and profile in project.participants.all():
            new_task = Tasks.objects.create(
                title=self.request.data["title"],
                description=self.request.data["description"],
                deadline=self.request.data["deadline"],
                project=project,
                status=TaskStatuses.objects.get(id=1),
                priority=Priorities.objects.get(id=self.request.data["priority"]),
            )
            
            profiles = Profile.objects.filter(id__in=self.request.data["assigned_to"])
            for i in profiles:
                new_task.assigned_to.add(i)
            new_task.save()

            for i in self.request.data["subtasks"]:
                new_subtask = Subtasks.objects.create(
                    task=new_task,
                    title=i.get("title"),
                    is_completed=False
                )
                new_subtask.save()
            return Response({"success": True})
        return Response({"success": False})

    @action(detail=False, methods=["GET"], name="Get My Tasks")
    def my(self, request):
        profile = Profile.objects.get(user=self.request.user.id)
        tasks = Tasks.objects.filter(project__participants__id=profile.id)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"], name="Get Task Details")
    def details(self, request):
        task = Tasks.objects.get(id=self.request.data["task_id"])
        serializer = TasksDetailSerializer(task)
        return Response(serializer.data)

    @action(detail=False, methods=["POST"], name="Edit Task Data")
    def edit(self, request):
        profile = Profile.objects.get(user=self.request.user.id)
        task = Tasks.objects.get(id=self.request.data["task_id"])
        project = Projects.objects.get(id=task.project.id)
        if profile.is_supervisor and profile in project.participants.all():
            profiles = Profile.objects.filter(id__in=self.request.data["assigned_to"])
            for i in profiles:
                task.assigned_to.add(i)
            task.title = self.request.data["title"]
            task.deadline = self.request.data["deadline"]
            task.description = self.request.data["description"]
            task.status = TaskStatuses.objects.get(id=self.request.data["status"])
            task.save()
            for i in self.request.data["subtasks"]:
                if i.get("id"):
                    subtask = Subtasks.objects.get(id=i.get("id"))
                    subtask.title = i.get("title")
                    subtask.is_completed = i.get("is_completed")
                    subtask.save()
                else:
                    new_subtask = Subtasks.objects.create(
                        task=task,
                        title=i.get("title"),
                        is_completed=False
                    )
                    new_subtask.save()
            return Response("Task edited")

        return Response("Task not edited")

    @action(detail=False, methods=["DELETE"], name="Delete Task")
    def delete(self, request):
        profile = Profile.objects.get(id=self.request.data["assigned_to"])
        if profile:
            if profile.is_supervisor:
                task = Tasks.objects.get(id=self.request.data["task_id"])
                task.delete()
                return Response("Task deleted")
            else:
                return Response("You are not a supervisor")
        return Response("You are not assigned to this task")


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

    @action(detail=False, methods=["POST"], name="Add student to supervisor")
    def add_student(self, request):
        profile = Profile.objects.get(user=self.request.user.id)
        if profile.is_supervisor:
            profile_student = Profile.objects.get(id=self.request.data["student_id"])
            profile_student.supervisor = profile.user
            profile_student.save()
            return Response("Student added")
        return Response("You are not a supervisor")


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

    @action(detail=False, methods=["POST"], name="Edit User Password")
    def change_password(self, request):
        user = User.objects.get(id=self.request.user.id)
        if not user.check_password(self.request.data["old_password"]):
            return HttpResponse(
                json.dumps({"status": "error", "error": "Wrong password"})
            )
        else:
            if self.request.data["new_password1"] != self.request.data["new_password2"]:
                return HttpResponse(
                    json.dumps({"status": "error", "error": "Password do not match"})
                )
            else:
                user.set_password(self.request.data["new_password1"])
                user.save()
                return HttpResponse(
                    json.dumps({"status": "OK", "message": "Password changed"})
                )


class AnalyticsPageViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = AnalyticsSerializer

    def get_queryset(self):
        profile = Profile.objects.filter(user=self.request.user)
        projects = Projects.objects.filter(id=self.request.data["project_id"])
        return projects

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

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user.id)
        if profile.is_supervisor:
            courses = Courses.objects.filter(course_supervisor=profile.id)
            return courses
        return Courses.objects.none()

    def create(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user.id)
        if profile.is_supervisor:
            new_course = Courses.objects.create(
                course_supervisor=profile, title=request.data["title"]
            )
            new_course.save()
            return Response("Course created")
        return Response("You are not a supervisor")

class UsersSearchViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        search_query = self.request.data["query"]
        supervisor_filter = self.request.data["is_supervisor"]
        if self.request.user.is_authenticated:
            return Profile.objects.filter(is_supervisor=supervisor_filter, user__username__icontains=search_query)[:10]

class SubtasksViewSet(viewsets.ModelViewSet):
    queryset = Subtasks.objects.all()
    serializer_class = SubtasksSerializer

    def get_queryset(self):
        return Subtasks.objects.filter(task=self.request.data["task_id"])

    def create(self, request, *args, **kwargs):
        task = Tasks.objects.get(id=self.request.data["task_id"])
        if task:
            new_subtask = Subtasks.objects.create(
                task=task,
                title=self.request.data["title"],
                is_completed=False
            )
            new_subtask.save()
            return Response("Subtask created")
        return Response("Task not found")

    def update(self, request, *args, **kwargs):
        subtask = Subtasks.objects.get(id=self.request.data["subtask_id"])
        if subtask:
            subtask.title = self.request.data["title"]
            subtask.description = self.request.data["description"]
            subtask.date = self.request.data["date"]
            subtask.status = TaskStatuses.objects.get(id=self.request.data["status"])
            subtask.save()
            return Response("Subtask edited")
        return Response("Subtask not found")

    def destroy(self, request, *args, **kwargs):
        subtask = Subtasks.objects.get(id=self.request.data["subtask_id"])
        if subtask:
            subtask.delete()
            return Response("Subtask deleted")
        return Response("Subtask not found")