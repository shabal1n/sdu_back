from django.contrib.auth.models import User, Group
from sdu.main.models import *
from rest_framework import serializers

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