from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views import View
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from main.models import *
from main.serializers import *
import datetime
from rest_framework import viewsets, permissions
from rest_framework.decorators import action


# Create your views here.

def json_response(request):
    return JsonResponse({"name": "Lucky"})

def http_response(request):
    return HttpResponse("<h1>Hello world!</h1>")

def say_hello(req):
    return HttpResponse("<h1>Hello Fleur</h1>")

# name: your name, email: your email, phone_number: your phone number


def user_profile(request):
    user_detail = {
        "name": "Lucky",
        "email": "lucky@email.com",
        "phone_number": "0445566777"
    }
    return JsonResponse(user_detail)


def filter_queries(request, query_id):
    query = {
        "id": query_id,
        "title": "Adama wants to take mental health break",
        "description": "My girlfriend gave me broken heart",
        "status": "DECLINED",
        "submitted_by": "Adama"
    }
    return JsonResponse(query)


class QueryView(View):
    queries = [
            {"id": 1, "title": "Adama declined Val shots"},
            {"id": 2, "title": "Samson declined Val shots"}
        ]
    def get(self, request):
        
        return JsonResponse({"result": self.queries})
    
    def post(self, request):
        return JsonResponse({"status": "ok"})
    


@api_view(["GET"])
def fetch_class_schedules(request):

    print("User making", request.user)
    # 1. Retrieve from db all class schedules
    queryset = ClassSchedule.objects.all()

    # 2. Return queryset result as response
    # 2b. Transform/serialize the queryset result to json and send as response

    serializer = ClassScheduleSerializer(queryset, many=True)

    # 3. Respond to the request
    return Response({"data": serializer.data}, status.HTTP_200_OK)

@api_view(["POST"])
def create_class_schedule(request):
    # Receiving data from frontend
    title = request.data.get("title")
    description = request.data.get("description")
    start_date_and_time = request.data.get("start_date_and_time")
    end_date_and_time = request.data.get("end_date_and_time")
    cohort_id = request.data.get("cohort_id")
    venue = request.data.get("venue")
    facilitator_id = request.data.get("facilitator_id")
    is_repeated = request.data.get("is_repeated", False)
    repeat_frequency = request.data.get("repeat_frequency", None)
    course_id = request.data.get("course_id")
    meeting_type = request.data.get("meeting_type")

    #Performing validations
    if not title:
        return Response({"message":"My friend, send me title"}, status.HTTP_400_BAD_REQUEST)
    
    cohort = None
    facilitator = None
    course = None

    #Validating the existence of records

    try:
        cohort = Cohort.objects.get(id=cohort_id)
    except Cohort.DoesNotExist:
        return Response({"message": "Massaa, this cohort does not exist"}, status.HTTP_400_BAD_REQUEST)
    
    try:
        facilitator = IMUser.objects.get(id=facilitator_id)
    except IMUser.DoesNotExist:
        return Response({"message": "Massaa, this facilitator does not exist"}, status.HTTP_400_BAD_REQUEST)
    
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response({"message": "Massaa, this course does not exist"}, status.HTTP_400_BAD_REQUEST)
    
    #creating class schedule
    class_schedule = ClassSchedule.objects.create(
        title=title,
        description=description,
        venue=venue,
        is_repeated=is_repeated,
        repeat_frequency=repeat_frequency,
        facilitator=facilitator,
        start_date_and_time=datetime.datetime.now(),
        end_date_and_time=datetime.datetime.now(),
        cohort=cohort,
        course=course,
        organizer=facilitator
    )
    class_schedule.save()

    serializer = ClassScheduleSerializer(class_schedule, many=False)
    return Response({"message": "Schedule successfully created", "data": serializer.data}, status.HTTP_201_CREATED)

class QueryModelViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=["post"])
    def raise_query(self, request):
        title = request.data.get("title")
        description = request.data.get("description", None)
        query_type = request.data.get("query_type")

        if not title or not description:
            return Response({"message": "My friend, send me title and description"}, status.HTTP_400_BAD_REQUEST)
        
        # if query_type == 'IT':
        #     assignee = IMUser.objects.get(username="admin")
        # else:
        #     assignee = IMUser.objects.get(username="operations")
        
        query = Query.objects.create(
            title=title,
            description=description,
            submitted_by=request.user,
            query_type=query_type
        )
        query.save()

        # Send email to assignee

        serializer = QuerySerializer(query, many=False)
        return Response({"message": "Query successfully raised", "data": serializer.data}, status.HTTP_201_CREATED)