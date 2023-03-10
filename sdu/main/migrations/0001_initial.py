# Generated by Django 4.1.4 on 2022-12-28 15:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Languages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Priorities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year_of_study', models.IntegerField()),
                ('birth_date', models.DateField()),
                ('language', models.CharField(max_length=2)),
                ('course_of_study', models.CharField(max_length=10)),
                ('picture_url', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25)),
                ('deadline', models.DateField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.courses')),
                ('priority', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.priorities')),
            ],
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Statuses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='StudyCases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25)),
                ('deadline', models.DateField()),
                ('description', models.CharField(max_length=100)),
                ('created_at', models.DateField()),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.profile')),
                ('priority', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.priorities')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.projects')),
                ('status', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.statuses')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.roles'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Attachments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25)),
                ('url', models.CharField(max_length=100)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.tasks')),
            ],
        ),
    ]
