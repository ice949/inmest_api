from django.urls import path
from .views import *

urlpatterns = [
    path('users/signup/', signup),
    path('users/login/', user_login),
    path('users/forgot_password/', ForgotPasswordView.as_view()),
]