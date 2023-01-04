from datetime import date
import django
from django.contrib.auth.models import User, Group
from sdu.main.models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import date

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups', 'password']

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    status = serializers.CharField(source='status.title')
    class Meta:
        model = Profile
        fields = [
            'username', 'email', 'year_of_study', 'status', 'birth_date', 
            'language', 'course_of_study', 'picture_url'
                ]


class ProjectsSerializer(serializers.ModelSerializer):
    participants = ProfileSerializer(many=True, read_only=True)
    class Meta:
        model = Projects
        fields = ['title', 'priority', 'deadline', 'course', 'participants']
        extra_kwargs = {
            'title': {'required': True},
            'priority': {'required': True},
            'deadline': {'required': True},
            'course': {'required': True},
            'participants': {'required': False}
        }

    def validate(self, attrs):
        if attrs['deadline'] < date.today():
            raise serializers.ValidationError("Deadline cannot be in the past")
        elif self.context['request'].user.profile.is_supervisor == 1: #TODO change to 0
            raise serializers.ValidationError("Only students can create projects")
        return attrs

    def create(self, validated_data):
        project = Projects.objects.create(**validated_data)
        project.participants.add(self.context['request'].user.profile)
        project.save()
        return project


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = [
                'title', 'assigned_to', 'deadline', 'created_at',
                'description', 'project', 'status'
                ]
        extra_kwargs = {
            'title': {'required': True},
            'assigned_to': {'required': False},
            'deadline': {'required': True},
            'created_at': {'required': False},
            'description': {'required': True},
            'project': {'required': True},
            'status': {'required': True}
        }

    def validate(self, attrs):
        if self.context['request'].user.profile.is_supervisor == 1: #TODO change to 0
            raise serializers.ValidationError("Only supervisors can create tasks")
        return attrs

    def create(self, validated_data):
        task = Tasks.objects.create(
                                title=validated_data['title'], deadline=validated_data['deadline'],
                                description=validated_data['description'], project=validated_data['project'], 
                                status=validated_data['status']
                                )
        task.assigned_to.add(self.context['request'].user.profile)
        task.save()
        return task
    

class ProfilePatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['birth_date', 'course_of_study', 'year_of_study']
        extra_kwargs = {
            'birth_date': {'required': True},
            'course_of_study': {'required': True},
            'year_of_study': {'required': True}
        }

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        token['username'] = user.username
        return token

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    profile = ProfilePatchSerializer()

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'profile')
        extra_kwargs = {
            'username': {'required': True},
            'password': {'required': True},
            'password2': {'required': True},
            'email': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs


    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        profile_data = validated_data.pop('profile')
        profile = Profile.objects.create(
                                         user=user,
                                         birth_date=profile_data['birth_date'],
                                         course_of_study=profile_data['course_of_study'],
                                         year_of_study=profile_data['year_of_study'])
        profile.save()

        return user