# Generated by Django 4.1.4 on 2023-01-03 09:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_profile_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='status',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='main.statuses'),
        ),
    ]
