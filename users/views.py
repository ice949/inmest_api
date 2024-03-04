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
    # new_user.generate_auth_token()
    serializer = AuthSerializer(new_user, many=False)
    return Response({"message": "Account successfully created", "result": serializer.data})

@api_view(["POST"])
@permission_classes([AllowAny])
def user_login(request):
    #1. Receive inputs/data from client and validate inputs
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"detail": "My friend behave yourself and send me username and password"}, status.HTTP_400_BAD_REQUEST)
    #2. Check user existence

    try:
        user = IMUser.objects.get(username=username)
        #3. User authentications
        auth_user = authenticate(username=username, password=password)
        if auth_user:
            if not user.is_active:
                return Response({"detail": "Your account is inactive. Please contact support."}, status.HTTP_403_FORBIDDEN)
            user.temporal_login_fail = 0
            user.save()
            #4. Login user
            login(request, user)
            serializer = AuthSerializer(user, many=False)
            return Response({"result": serializer.data }, status.HTTP_200_OK)

        else:
            user.temporal_login_fail += 1
            user.save()
            return Response({"detail": "Invalid credentials"}, status.HTTP_400_BAD_REQUEST)

    except IMUser.DoesNotExist:
        return Response({"detail": "Username does not exist"}, status.HTTP_400_BAD_REQUEST)
    


class UserViewSet(viewsets.ModelViewSet):
  
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password', None)
        player_id = request.data.get('player_id', None)
    
        user = authenticate(email=email, password=password)
        login(request, user)

        