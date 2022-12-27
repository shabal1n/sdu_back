from django.db import models
from django.contrib.auth.models import User

class Courses(models.Model):
    title = models.CharField(max_length=25, blank=False)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

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
    sdu_id = models.CharField(max_length=9, blank=False)
    admission_year = models.IntegerField(blank=False)
    sdu_mail = models.EmailField(max_length=24, blank=False)
    language = models.CharField(max_length=2, blank=False)
    case_of_study = models.ForeignKey(StudyCases, blank=False, on_delete=models.CASCADE)
    role = models.OneToOneField(Roles, blank=False, on_delete=models.CASCADE)
    picture_url = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.user.first_name + self.user.last_name

class Projects(models.Model):
    title = models.CharField(max_length=25, blank=False)
    priority = models.OneToOneField(Priorities, blank=False, on_delete=models.CASCADE)
    deadline = models.DateField(blank=False)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + " " + self.course.title

class Tasks(models.Model):
    title = models.CharField(max_length=25, blank=False)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(Profile, on_delete=models.CASCADE)
    priority = models.OneToOneField(Priorities, blank=False, on_delete=models.CASCADE)
    deadline = models.DateField(blank=False)
    description = models.CharField(max_length=100, blank=False)
    created_at = models.DateField(blank=False)
    status = models.OneToOneField(Statuses, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.project.title + " " + self.title

class Attachments(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    title = models.CharField(max_length=25, blank=False)
    url = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.task.title + " " + self.title