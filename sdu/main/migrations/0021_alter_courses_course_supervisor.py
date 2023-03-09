# Generated by Django 4.1.4 on 2023-03-09 09:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0020_courses_course_supervisor"),
    ]

    operations = [
        migrations.AlterField(
            model_name="courses",
            name="course_supervisor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="course_supervisor",
                to="main.profile",
            ),
        ),
    ]
