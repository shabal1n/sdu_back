import datetime
import os
from django.db import models
from django.contrib.auth.models import User


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


class UserStatuses(models.Model):
    title = models.CharField(max_length=25, blank=False)

    def __str__(self):
        return self.title


def image_name(instance, filename):
    return os.path.join("profile_pics", filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=image_name, blank=True)
    year_of_study = models.CharField(blank=True, max_length=9)
    birth_date = models.CharField(blank=False, max_length=10)
    language = models.CharField(max_length=2, blank=False, default="en")
    course_of_study = models.CharField(max_length=10, blank=True)
    status = models.ForeignKey(
        UserStatuses, blank=True, on_delete=models.CASCADE, default=1
    )
    is_supervisor = models.BooleanField(default=False)
    supervisor = models.ForeignKey(
        "self", on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return self.user.username


class Courses(models.Model):
    course_supervisor = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True
    )
    title = models.CharField(max_length=25, blank=False)

    def __str__(self):
        return self.title


class Projects(models.Model):
    title = models.CharField(max_length=25, blank=False)
    priority = models.ForeignKey(Priorities, blank=False, on_delete=models.CASCADE)
    deadline = models.DateField(blank=False)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    participants = models.ManyToManyField(Profile)

    def __str__(self):
        return self.title + " " + self.course.title


class TaskStatuses(models.Model):
    title = models.CharField(max_length=25, blank=False)

    def __str__(self):
        return self.title


class Tasks(models.Model):
    title = models.CharField(max_length=25, blank=False)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    assigned_to = models.ManyToManyField(Profile)
    deadline = models.DateField(blank=False)
    description = models.CharField(max_length=100, blank=False)
    created_at = models.DateField(blank=False, default=datetime.date.today)
    completed_at = models.DateField(blank=True, null=True)
    status = models.ForeignKey(TaskStatuses, blank=False, on_delete=models.CASCADE)
    priority = models.ForeignKey(
        Priorities, blank=False, on_delete=models.CASCADE, default=1
    )

    def __str__(self):
        return self.project.title + " " + self.title


class Subtasks(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    title = models.CharField(max_length=25, blank=False)
    is_completed = models.BooleanField(blank=False, null=False, default=False)

    def __str__(self):
        return self.task.title + " " + self.title


class Attachments(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    title = models.CharField(max_length=25, blank=False)
    url = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.task.title + " " + self.title
