from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token

# Create your models here.

class IMUser(AbstractUser):
    USER_TYPES = (
        ('EIT', 'EIT'),
        ('TEACHING_FELLOW', 'TEACHING FELLOW'),
        ('ADMIN_STAFF', 'ADMINISTRATIVE STAFF'),
        ('ADMIN', 'ADMINSTRATOR'),
    )
    first_name = models.CharField(max_length=155, blank=True)
    last_name = models.CharField(max_length=155, blank=True)
    middle_name = models.CharField(max_length=155, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='EIT')
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    unique_code = models.CharField(max_length=4, blank=True)
    is_blocked = models.BooleanField(default=False)
    temporal_login_fail = models.IntegerField(default=0)
    permanent_login_fail = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
@receiver(post_save, sender=IMUser)
def generate_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        token = Token.objects.create(user=instance)
        token.save()


class Cohort(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    year = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(IMUser, related_name="cohort_author", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.year})"
    
class CohortMember(models.Model):
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE, related_name='cohort')
    member = models.ForeignKey(IMUser, on_delete=models.CASCADE, related_name='cohort_member')
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(IMUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.member.first_name} {self.member.last_name} ({self.cohort.name})"