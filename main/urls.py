from django.urls import path
from .views import *

urlpatterns = [
    path("say_hello/", say_hello),
    path("profile/", user_profile),
    path("filter_queries/<int:query_id>/", filter_queries),
    path("queries/", QueryView.as_view(), name="query-view"),
    path("schedules/fetch/", fetch_class_schedules),
    path("schedules/create/", create_class_schedule)
]
