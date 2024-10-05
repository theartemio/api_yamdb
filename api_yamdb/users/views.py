import random
import re
from http import HTTPStatus
from rest_framework import status, viewsets, permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
# from .models import User
from django.contrib.auth import authenticate, get_user_model

from .serializers import RegistrationSerializer, LoginSerializer, UsersSerializer

User = get_user_model()


class RegistrationAPIView(APIView):
    """
    Разрешить всем пользователям (аутентифицированным и нет) доступ к данному эндпоинту.
    """
    # permission_classes = (AllowAny,)
    # serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            pattern = r'^[\w.@+-]+\Z'
            if request.data['username'] == 'me' or not re.fullmatch(pattern, request.data['username']):
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.get(username=request.data['username'])
            if user.email != request.data['email']:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            confirmation_code = random.randint(1000, 9999)
            users_email = self.request.data['email']
            send_mail(
                subject='Code',
                message=f'confirmation code: {confirmation_code}',
                from_email='api@yamdb.not',
                recipient_list=[users_email],
                fail_silently=True,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        """ if request.data['username'] != User.objects.get(username=request.data['username']):
            return Response(status=status.HTTP_404_NOT_FOUND) """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UsersAPIView(APIView):

    def get(self, request):
        pass

    def post(self, request):
        serializer = UsersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
