import datetime
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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_pics', blank=True)
    year_of_study = models.CharField(blank=True, max_length=9)
    birth_date = models.CharField(blank=False, max_length=10)
    language = models.CharField(max_length=2, blank=False, default="en")
    course_of_study = models.CharField(max_length=10, blank=True)
    status = models.ForeignKey(
        UserStatuses, blank=True, on_delete=models.CASCADE, default=1
    )
    is_supervisor = models.BooleanField(default=False)
    picture_url = models.CharField(max_length=100, blank=True)
    supervisor = models.ForeignKey(
        User, related_name="supervisor", on_delete=models.CASCADE, null=True, blank=True
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

class FriendsList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, related_name="friends")

    def __str__(self):
        return self.user.username

    def remove_friend(self, friend):
        self.friends.remove(friend)

    def add_friend(self, friend):
        self.friends.add(friend)

    def unfriend(self, friend):
        self.remove_friend(friend)
        FriendsList.objects.get(user=friend).remove_friend(self.user)

    def is_mutual_friend(self, friend):
        if friend in self.friends.all():
            return True
        return False


class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="from_user"
    )
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")
    is_active = models.BooleanField(default=True, blank=True, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.from_user.username + " " + self.to_user.username

    def accept(self):
        self.is_active = False
        self.save()
        friend_list, created = FriendsList.objects.get_or_create(user=self.from_user)
        friend_list.add_friend(self.to_user)
        friend_list, created = FriendsList.objects.get_or_create(user=self.to_user)
        friend_list.add_friend(self.from_user)

    def decline(self):
        self.is_active = False
        self.save()

    def get_from_user(self):
        return self.from_user


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
