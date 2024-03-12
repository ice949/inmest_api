from django.db import models
import datetime
from users.models import *

# Create your models here.

class Course(models.Model):
    name=models.CharField(max_length=1000)
    description = models.TextField(default='N/A', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class ClassSchedule(models.Model):
    REPEAT_FREQUENCIES = (
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
    )
    MEETING_TYPES = (
        ('CLASS_SESSION', 'Class Sessions'),
        ('WELLNESS_SESSION', 'Well Session'),
        ('GUEST_LECTURE', 'Guest Lecture'),
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date_and_time = models.DateTimeField()
    end_date_and_time = models.DateTimeField()
    is_repeated = models.BooleanField(default=False)
    repeat_frequency = models.CharField(max_length=20, choices=REPEAT_FREQUENCIES, blank=True, null=True)
    meeting_type = models.CharField(max_length=20, choices=MEETING_TYPES, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    organizer = models.ForeignKey(IMUser, on_delete=models.CASCADE, related_name='organized_classes')  
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE, related_name='class_schedules') 
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True, related_name='class_schedule_course') 
    facilitator = models.ForeignKey(IMUser, on_delete=models.SET_NULL, blank=True, null=True, related_name='class_schedule_facilitator') 
    venue = models.CharField(max_length=255, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.cohort.name})"

class ClassAttendance(models.Model):
    class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE, related_name='attendances')
    attendee = models.ForeignKey(IMUser, on_delete=models.CASCADE, related_name='attended_classes')  
    is_present = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(IMUser, on_delete=models.CASCADE)  # Assuming IMUser from Part 1
    

    def __str__(self):
        return f"{self.class_schedule.title}: {self.attendee.first_name} {self.attendee.last_name}"

class Query(models.Model):
    RESOLUTION_STATUSES = (
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('DECLINED', 'Declined'),
        ('RESOLVED', 'Resolved'), 
    )

    QUERY_TYPES = (
        ('OPERATIONS', 'Operations'),
        ('IT', 'IT'),
        ('KITCHEN', 'Kitchen'),
        ('SECURITY', 'Security'),

    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    submitted_by = models.ForeignKey(IMUser, on_delete=models.CASCADE, related_name='submitted_queries')
    assigned_to = models.ForeignKey(IMUser, on_delete=models.CASCADE, related_name='assigned_queries', blank=True, null=True)
    resolution_status = models.CharField(max_length=30, choices=RESOLUTION_STATUSES, default='PENDING')
    query_type = models.CharField(max_length=30, choices=QUERY_TYPES, default='OPERATIONS')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(IMUser, on_delete=models.CASCADE, related_name="query_author")

    def __str__(self):
        return f"{self.title} (Submitted by: {self.submitted_by.email})"

class QueryComment(models.Model):
    query = models.ForeignKey(Query, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(IMUser, on_delete=models.CASCADE) 

    def __str__(self):
        return f"Comment on {self.query.title} ({self.author.username})"