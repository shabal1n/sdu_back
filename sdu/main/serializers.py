from django.contrib.auth.models import User, Group
from sdu.main.models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups', 'password']


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'sdu_id', 'admission_year', 'sdu_id', 'sdu_mail', 'language', 'case_of_study', 
        'role', 'picture_url']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class CoursesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Courses
        fields = ['url', 'title', 'teacher']

class RolesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Roles
        fields = ['url', 'title']

class PrioritiesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Priorities
        fields = ['title']

class AttachmentsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attachments
        fields = ['url', 'task', 'title', 'url']

class StudyCasesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StudyCases
        fields = ['url', 'title']
    
class TasksSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tasks
        fields = ['url', 'title', 'project', 'assigned_to', 'priority', 'deadline',
         'description', 'created_at', 'status']

class ProjectsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Projects
        fields = ['url', 'title', 'priority', 'deadline', 'course']

class StatusesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Statuses
        fields = ['url', 'title']

class TasksSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tasks
        fields = ['url', 'title', 'project', 'assigned_to', 'priority', 'deadline',
         'description', 'created_at', 'status']

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