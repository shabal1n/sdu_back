import datetime
from django.db import models
from django.contrib.auth.models import User

class Courses(models.Model):
    title = models.CharField(max_length=25, blank=False)

    def __str__(self):
        return self.title

class Roles(models.Model):
    title = models.CharField(max_length=25, blank=False)
    
    def __str__(self):
        return self.title

class StudyCases(models.Model):
    title = models.CharField(max_length=25, blank=False)

    def __str__(self):
        return self.title

class Priorities(models.Model):
    title = models.CharField(max_length=25, blank=False)
    def __str__(self):
        return self.title

class Languages(models.Model):
    title = models.CharField(max_length=2, blank=False)

    def __str__(self):
        return self.title

class Statuses(models.Model):
    title = models.CharField(max_length=25, blank=False)

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    year_of_study = models.CharField(blank=False, max_length=9)
    birth_date = models.CharField(blank=False, max_length=10)
    language = models.CharField(max_length=2, blank=False, default="en")
    course_of_study = models.CharField(max_length=10, blank=False)
    status = models.ForeignKey(Statuses, blank=True, on_delete=models.CASCADE, default=1)
    is_supervisor = models.BooleanField(default=False)
    picture_url = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.user.first_name + self.user.last_name

class Projects(models.Model):
    title = models.CharField(max_length=25, blank=False)
    priority = models.ForeignKey(Priorities, blank=False, on_delete=models.CASCADE)
    deadline = models.DateField(blank=False)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    participants = models.ManyToManyField(Profile)

    def __str__(self):
        return self.title + " " + self.course.title

class Tasks(models.Model):
    title = models.CharField(max_length=25, blank=False)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    assigned_to = models.ManyToManyField(Profile)
    deadline = models.DateField(blank=False)
    description = models.CharField(max_length=100, blank=False)
    created_at = models.DateField(blank=False, default=datetime.date.today)
    status = models.CharField(max_length=20, blank=False, default="New")

    def __str__(self):
        return self.project.title + " " + self.title

class Attachments(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    title = models.CharField(max_length=25, blank=False)
    url = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.task.title + " " + self.title