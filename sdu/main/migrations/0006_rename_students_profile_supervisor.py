# Generated by Django 3.2.18 on 2023-03-24 05:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20230324_0508'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='students',
            new_name='supervisor',
        ),
    ]
