# Generated by Django 4.1.4 on 2022-12-28 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='year_of_study',
            field=models.CharField(max_length=9),
        ),
    ]
