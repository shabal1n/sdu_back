# Generated by Django 4.1.4 on 2023-01-10 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_taskstatuses_rename_statuses_userstatuses_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='completed_at',
            field=models.DateField(blank=True, null=True),
        ),
    ]
