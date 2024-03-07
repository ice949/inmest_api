from django.shortcuts import render
from .models import *
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes, action
from .serializers import *
from rest_framework import status
from inmest_api.utils import *

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    username = request.data.get("username")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")
    phone_number = request.data.get("phone_number")
    password = request.data.get("password")
    new_user = IMUser.objects.create(
        username=username,
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number
        )
    new_user.set_password(password)
    new_user.save()
    
    serializer = AuthSerializer(new_user, many=False)
    return Response({"message": "Account successfully created", "result": serializer.data})

@api_view(["POST"])
@permission_classes([AllowAny])
def user_login(request):
    
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"detail": "My friend behave yourself and send me username and password"}, status.HTTP_400_BAD_REQUEST)
    

    try:
        user = IMUser.objects.get(username=username)
        
        auth_user = authenticate(username=username, password=password)
        if auth_user:
            if not user.is_active:
                return Response({"detail": "Your account is inactive. Please contact support."}, status.HTTP_403_FORBIDDEN)
            user.temporal_login_fail = 0
            user.save()
            
            login(request, user)
            serializer = AuthSerializer(user, many=False)
            return Response({"result": serializer.data }, status.HTTP_200_OK)

        else:
            if user.temporal_login_fail >= 5:
                user.is_active = False
                user.save()
                return Response({"detail": "Your account has been locked. Please contact support."}, status.HTTP_403_FORBIDDEN)
            
            user.temporal_login_fail += 1
            user.save()
            return generate_400_response("Invalid username or password")

    except IMUser.DoesNotExist:
        return Response({"detail": "Username does not exist"}, status.HTTP_400_BAD_REQUEST)
    

class ForgotPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        if not email:
            return generate_400_response("Please provide an email")
        
        try:
            user = IMUser.objects.get(Q(username=email) | Q(email=email))
            otp_code = generate_unique_code()
            user.unique_code = otp_code
            user.save()
            user.send_reset_password_email(otp_code)
            return Response({"detail": "An email with the otp has been sent to your email address"}, status.HTTP_200_OK)
        except IMUser.DoesNotExist:
            return generate_400_response("User does not exist")

# class ForgotPasswordView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         email = request.data.get("email")
#         if not email:
#             return Response({"detail": "Please provide an email"}, status.HTTP_400_BAD_REQUEST)
        
#         user = IMUser.objects.filter(Q(username=email) | Q(email=email)).first()
#         if not user:
#             return Response({"detail": "User does not exist"}, status.HTTP_400_BAD_REQUEST)
        
#         user.send_reset_password_email()
#         return Response({"detail": "An email has been sent to your email address"}, status.HTTP_200_OK)

        