import datetime
import calendar
from rest_framework import exceptions
from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from django.contrib.auth.models import User
from sdu.main.models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.validators import EmailValidator

from sdu.main.validation import validateEmail, APIException200, UniqueValidator


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["profile_id", "username", "email"]

    def get_profile_id(self, obj):
        return Profile.objects.get(user=obj).id


class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = ["id", "title", "course_supervisor"]


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(
        source="user.email",
        read_only=True,
        validators=[
            UniqueValidator(queryset=Profile.objects.all()),
            EmailValidator(message="Invalid Email"),
        ],
    )
    status = serializers.CharField(source="status.title")

    class Meta:
        model = Profile
        fields = [
            "id",
            "username",
            "email",
            "year_of_study",
            "status",
            "birth_date",
            "language",
            "course_of_study",
            "photo",
        ]


class ProjectsSerializer(serializers.ModelSerializer):
    participants = ProfileSerializer(many=True, read_only=True)
    complete_tasks = serializers.SerializerMethodField()
    total_tasks = serializers.SerializerMethodField()

    class Meta:
        model = Projects
        fields = [
            "id",
            "title",
            "priority",
            "deadline",
            "course",
            "participants",
            "complete_tasks",
            "total_tasks",
        ]
        extra_kwargs = {
            "title": {"required": True},
            "priority": {"required": True},
            "deadline": {"required": True},
            "course": {"required": True},
            "participants": {"required": False},
        }

    def validate(self, attrs):
        if attrs["deadline"] < date.today():
            raise exceptions.ValidationError("Deadline cannot be in the past")
        elif self.context["request"].user.profile.is_supervisor == 0:
            raise exceptions.ValidationError("Only supervisors can create projects")
        return attrs

    def create(self, validated_data):
        project = Projects.objects.create(**validated_data)
        project.participants.add(self.context["request"].user.profile)
        for user in self.context["request"].data["participants"]:
            project.participants.add(Profile.objects.get(id=user))
        project.save()
        return project

    def get_complete_tasks(self, obj):
        return Tasks.objects.filter(project=obj, status=3).count()

    def get_total_tasks(self, obj):
        return Tasks.objects.filter(project=obj).count()


class PrioritiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Priorities
        fields = "__all__"


class TasksSerializer(serializers.ModelSerializer):
    assigned_to = ProfileSerializer(read_only=True, many=True)
    subtasks_quantity = serializers.SerializerMethodField()
    completed_subtasks_quantity = serializers.SerializerMethodField()
    subtasks = serializers.SerializerMethodField()
    superviors = serializers.SerializerMethodField()

    class Meta:
        model = Tasks
        fields = [
            "title",
            "assigned_to",
            "deadline",
            "created_at",
            "description",
            "project",
            "status",
            "priority",
            "subtasks_quantity",
            "subtasks",
            "completed_subtasks_quantity",
            "superviors",
        ]
        extra_kwargs = {
            "title": {"required": True},
            "assigned_to": {"required": False},
            "deadline": {"required": True},
            "created_at": {"required": False},
            "description": {"required": True},
            "project": {"required": True},
            "status": {"required": True},
        }

    def validate(self, attrs):
        if self.context["request"].user.profile.is_supervisor == 0:
            raise exceptions.ValidationError("Only supervisors can create tasks")
        return attrs

    def get_subtasks(self, obj):
        return SubtasksSerializer(obj.subtasks_set.all(), many=True).data

    def get_subtasks_quantity(self, obj):
        return Subtasks.objects.filter(task=obj).count()

    def get_completed_subtasks_quantity(self, obj):
        return Subtasks.objects.filter(task=obj, is_completed=1).count()

    def get_superviors(self, obj):
        supervisors = []
        for profile in obj.project.participants.all():
            if profile.is_supervisor:
                supervisors.append(profile)
        print(supervisors)
        return ProfileSerializer(supervisors, many=True).data

    def create(self, validated_data):
        task = Tasks.objects.create(
            title=validated_data["title"],
            deadline=validated_data["deadline"],
            description=validated_data["description"],
            project=validated_data["project"],
            status=validated_data["status"],
        )
        task.assigned_to.add(self.context["request"].user.profile)
        task.save()
        return task


class SubtasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtasks
        fields = ["id", "title", "task", "is_completed"]
        extra_kwargs = {
            "id": {"required": False},
            "title": {"required": True},
            "task": {"required": True},
            "is_completed": {"required": False},
        }


class TasksDetailSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SerializerMethodField()
    project = serializers.SerializerMethodField()
    subtasks = serializers.SerializerMethodField()

    class Meta:
        model = Tasks
        fields = "__all__"

    def get_assigned_to(self, obj):
        return ProfileSerializer(obj.assigned_to.all(), many=True).data

    def get_project(self, obj):
        return ProjectsSerializer(obj.project).data

    def get_subtasks(self, obj):
        return SubtasksSerializer(obj.subtasks_set.all(), many=True).data


class ProfilePatchSerializer(serializers.ModelSerializer):
    birth_date = serializers.CharField()
    course_of_study = serializers.CharField()
    year_of_study = serializers.CharField()

    class Meta:
        model = Profile
        fields = ["birth_date", "course_of_study", "year_of_study"]


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token["username"] = user.username
        token["email"] = user.email
        return token

    def validate(self, attrs):
        userName = attrs.get("username")
        password = attrs.get("password")

        if validateEmail(userName) is True:
            try:
                user = User.objects.get(email=userName)
                if user.check_password(password):
                    attrs["username"] = user.username

            except User.DoesNotExist:
                raise exceptions.AuthenticationFailed(
                    "No such user with provided credentials".title()
                )

        data = super().validate(attrs)
        return data


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.CharField(
        write_only=True,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    password = serializers.CharField(write_only=True, required=True, validators=None)
    username = serializers.CharField(
        write_only=True,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password2 = serializers.CharField(write_only=True, required=True, validators=None)
    profile = ProfilePatchSerializer()

    class Meta:
        model = User
        fields = ("username", "password", "password2", "email", "profile")
        extra_kwargs = {
            "username": {"required": True},
            "password": {"required": True},
            "password2": {"required": True},
            "email": {"required": True},
        }

    def validate(self, attrs):
        min_length = 6
        password = attrs["password"]
        if password != attrs["password2"]:
            raise APIException200(
                detail={
                    "status": "error",
                    "error": {"password": "Passwords must match!!"},
                }
            )
        if len(password) < min_length:
            raise APIException200(
                detail={
                    "status": "error",
                    "error": {"password": "Passwords length must be more than 6."},
                }
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data.pop("username"), email=validated_data["email"]
        )
        user.set_password(validated_data.pop("password"))
        user.save()
        profile_data = validated_data["profile"]
        profile = Profile.objects.create(
            user=user,
            birth_date=profile_data["birth_date"],
            course_of_study=profile_data["course_of_study"],
            year_of_study=profile_data["year_of_study"],
        )
        profile.save()

        return user


class DashboardSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    is_advisor = serializers.SerializerMethodField()
    complete_tasks = serializers.SerializerMethodField()
    total_tasks = serializers.SerializerMethodField()
    in_progress_tasks = serializers.SerializerMethodField()
    proposed_tasks = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()
    students = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = "__all__"

    def get_username(self, obj):
        return self.context["request"].user.username

    def get_email(self, obj):
        return self.context["request"].user.email

    def get_is_advisor(self, obj):
        if obj.is_supervisor == 1:
            return "Supervisor"
        return "Student"

    def get_total_tasks(self, obj):
        return Tasks.objects.filter(assigned_to=obj).count()

    def get_complete_tasks(self, obj):
        return Tasks.objects.filter(assigned_to=obj, status=3).count()

    def get_in_progress_tasks(self, obj):
        return Tasks.objects.filter(assigned_to=obj, status=2).count()

    def get_proposed_tasks(self, obj):
        return Tasks.objects.filter(assigned_to=obj, status=1).count()

    def get_projects(self, obj):
        projects = Projects.objects.filter(participants=obj)
        return ProjectsSerializer(projects, many=True).data

    def get_students(self, obj):
        if obj.is_supervisor:
            students = Profile.objects.filter(supervisor=obj)
            return ProfileSerializer(students, many=True).data
        return False


class ProfilePageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    is_advisor = serializers.CharField(source="profile.is_advisor", read_only=True)
    status = serializers.CharField(source="status.title")
    complete_tasks = serializers.SerializerMethodField()
    pending_tasks = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()
    total_tasks = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "username",
            "is_advisor",
            "status",
            "complete_tasks",
            "pending_tasks",
            "projects",
            "total_tasks",
        ]

    def get_complete_tasks(self, obj):
        return Tasks.objects.filter(assigned_to=obj, status=3).count()

    def get_pending_tasks(self, obj):
        return Tasks.objects.filter(assigned_to=obj, status=2).count()

    def get_projects(self, obj):
        return Projects.objects.filter(participants=obj).count()

    def get_total_tasks(self, obj):
        return Tasks.objects.filter(assigned_to=obj).count()


class AnalyticsSerializer(serializers.ModelSerializer):
    project = serializers.CharField(source="title")
    participants = serializers.SerializerMethodField()
    assigned_tasks = serializers.SerializerMethodField()
    tasks_count_by_days = serializers.SerializerMethodField()
    completed_tasks = serializers.SerializerMethodField()

    class Meta:
        model = Projects
        fields = "__all__"

    def get_participants(self, obj):
        return ProfileSerializer(obj.participants.all(), many=True).data

    def get_assigned_tasks(self, obj):
        request = self.context.get("request")
        start_date = request.query_params["start_date"]
        end_date = request.query_params["end_date"]
        if len(start_date) == 0:
            start_date = datetime.datetime.now() - datetime.timedelta(days=30)
        if len(end_date) == 0:
            end_date = datetime.datetime.now()

        return Tasks.objects.filter(
            assigned_to=self.context["request"].user.profile,
            project=obj,
            created_at__range=[start_date, end_date],
        ).count()

    def get_completed_tasks(self, obj):
        request = self.context.get("request")
        start_date = request.query_params["start_date"]
        end_date = request.query_params["end_date"]
        if len(start_date) == 0:
            start_date = datetime.datetime.now() - datetime.timedelta(days=30)
        if len(end_date) == 0:
            end_date = datetime.datetime.now()

        return Tasks.objects.filter(
            assigned_to=self.context["request"].user.profile,
            project=obj,
            completed_at__range=[start_date, end_date],
        ).count()

    def get_tasks_count_by_days(self, obj):
        request = self.context.get("request")
        start_date = request.query_params["start_date"]
        end_date = request.query_params["end_date"]
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        if start_date:
            start_date = datetime.datetime.now() - datetime.timedelta(days=30)
        if end_date:
            end_date = datetime.datetime.now()

        tasks_of_project = Tasks.objects.filter(project=obj)
        tasks_count_by_days = {}
        while start_date <= end_date:
            tasks_count_by_days[start_date.strftime("%m-%d")] = tasks_of_project.filter(
                created_at=start_date
            ).count()
            start_date += datetime.timedelta(days=1)
        return tasks_count_by_days


class AnalyticsExtendedSerializer(serializers.ModelSerializer):
    project = serializers.CharField(source="title")
    assigned_tasks = serializers.SerializerMethodField()
    tasks_count_by_days = serializers.SerializerMethodField()
    completed_tasks = serializers.SerializerMethodField()
    tasks_by_hours = serializers.SerializerMethodField()
    tasks_this_month = serializers.SerializerMethodField()
    completed_this_month = serializers.SerializerMethodField()
    completed_today = serializers.SerializerMethodField()
    tasks_this_year = serializers.SerializerMethodField()
    completed_this_year = serializers.SerializerMethodField()

    class Meta:
        model = Projects
        fields = [
            "project",
            "assigned_tasks",
            "tasks_count_by_days",
            "completed_tasks",
            "tasks_by_hours",
            "completed_today",
            "completed_this_month",
            "tasks_this_month",
            "tasks_this_year",
            "completed_this_year",
        ]

    def get_assigned_tasks(self, obj):
        return Tasks.objects.filter(
            assigned_to=self.context["request"].user.profile,
            project=obj,
        ).count()

    def get_completed_tasks(self, obj):
        return Tasks.objects.filter(
            assigned_to=self.context["request"].user.profile,
            status=3,
            project=obj,
        ).count()

    def get_tasks_count_by_days(self, obj):  # TODO check if correct
        tasks_of_project = Tasks.objects.filter(project=obj)
        today_weekday = datetime.datetime.now()
        tasks_count_by_days = {}
        for i in range(6, 0, -1):
            day = today_weekday - datetime.timedelta(days=i)
            tasks_count_by_days[day.weekday()] = tasks_of_project.filter(
                created_at=day
            ).count()
        tasks_count_by_days[today_weekday.weekday()] = tasks_of_project.filter(
            created_at=today_weekday
        ).count()
        return tasks_count_by_days

    def get_tasks_by_hours(self, obj):
        tasks_of_project = Tasks.objects.filter(project=obj)
        today = datetime.datetime.now()
        tasks_count_by_hours = {}
        for i in range(23, 0, -1):
            hour = today - datetime.timedelta(hours=i)
            tasks_count_by_hours[hour.hour] = tasks_of_project.filter(
                created_at=hour
            ).count()
        tasks_count_by_hours[today.hour] = tasks_of_project.filter(
            created_at=today
        ).count()
        return tasks_count_by_hours

    def get_completed_this_month(self, obj):
        today = datetime.datetime.now()
        return Tasks.objects.filter(
            assigned_to=self.context["request"].user.profile,
            created_at__month=today.month,
            project=obj,
        ).count()

    def get_tasks_this_month(self, obj):
        tasks_of_project = Tasks.objects.filter(project=obj)
        today = datetime.datetime.now()
        month_days = calendar.monthrange(today.year, today.month)[1]
        tasks_count_by_this_month = {}
        for i in range(month_days, 0, -1):
            day = today - datetime.timedelta(days=i)
            tasks_count_by_this_month[day.day] = tasks_of_project.filter(
                created_at=day
            ).count()
        return tasks_count_by_this_month

    def get_tasks_this_year(self, obj):
        tasks_of_project = Tasks.objects.filter(project=obj)
        today = datetime.datetime.now()
        tasks_count_by_this_year = {}
        for i in range(12, 0, -1):
            month = today - relativedelta(months=-i)
            tasks_count_by_this_year[month.month] = tasks_of_project.filter(
                created_at__month=month.month
            ).count()
        return tasks_count_by_this_year

    def get_completed_this_year(self, obj):
        today = datetime.datetime.now()
        return Tasks.objects.filter(
            assigned_to=self.context["request"].user.profile,
            status=3,
            completed_at__year=today.year,
            project=obj,
        ).count()

    def completed_this_week(self, obj):
        today = datetime.datetime.now()
        return Tasks.objects.filter(
            assigned_to=self.context["request"].user.profile,
            status=3,
            completed_at__week=today.weekday,
            project=obj,
        ).count()

    def get_completed_today(self, obj):
        today = datetime.datetime.now()
        return Tasks.objects.filter(
            assigned_to=self.context["request"].user.profile,
            status=3,
            completed_at=today,
            project=obj,
        ).count()
