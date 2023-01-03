# Generated by Django 4.1.4 on 2023-01-03 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_profile_is_supervisor'),
    ]

    operations = [
        migrations.AddField(
            model_name='projects',
            name='participants',
            field=models.ManyToManyField(to='main.profile'),
        ),
        migrations.RemoveField(
            model_name='tasks',
            name='assigned_to',
        ),
        migrations.AddField(
            model_name='tasks',
            name='assigned_to',
            field=models.ManyToManyField(to='main.profile'),
        ),
    ]
