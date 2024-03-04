from django.contrib import admin
from .models import *

# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    list_display=("name", "date_created", "date_modified")


admin.site.register(Course, CourseAdmin)