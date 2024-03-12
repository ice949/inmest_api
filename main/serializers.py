from rest_framework import serializers
from main.models import *
from users.serializers import *
class CourseModelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'description')
        model = Course

class CourseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    date_created = serializers.DateTimeField()

class ClassScheduleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    start_date_and_time = serializers.DateTimeField()
    end_date_and_time = serializers.DateTimeField()
    is_repeated = serializers.BooleanField()
    repeat_frequency = serializers.CharField()
    organizer = UserSerializer(many=False)
    meeting_type = serializers.CharField()
    facilitator = UserSerializer(many=False)
    venue = serializers.CharField()
    course = CourseSerializer(many=False)
    cohort = CohortSerializer(many=False)
    date_created = serializers.DateTimeField()

class QuerySerializer(serializers.Serializer):
    cohort_id = serializers.IntegerField()
    course_id = serializers.IntegerField()
    facilitator_id = serializers.IntegerField()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
