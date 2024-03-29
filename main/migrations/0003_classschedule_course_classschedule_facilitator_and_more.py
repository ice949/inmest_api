# Generated by Django 5.0.1 on 2024-02-22 10:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='classschedule',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='class_schedule_course', to='main.course'),
        ),
        migrations.AddField(
            model_name='classschedule',
            name='facilitator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='class_schedule_facilitator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='classschedule',
            name='meeting_type',
            field=models.CharField(blank=True, choices=[('CLASS_SESSION', 'Class Sessions'), ('WELLNESS_SESSION', 'Well Session'), ('GUEST_LECTURE', 'Guest Lecture')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='query',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='query_author', to=settings.AUTH_USER_MODEL),
        ),
    ]
