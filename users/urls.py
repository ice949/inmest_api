from django.urls import path
from .views import *

urlpatterns = [
    path('users/signup/', signup),
    path('users/login/', user_login),
    path('users/forgot_password/', ForgotPasswordApiView.as_view()),
    path('users/reset_password/', ResetPasswordApiView.as_view()),
    path('users/change_password/', ChangePasswordApiView.as_view()),
    path('users/current_user/', GetCurrentUserProfile.as_view()),
]