import random
import re
from http import HTTPStatus

# from .models import User
from django.contrib.auth import authenticate, get_user_model
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import (filters, generics, mixins, permissions, status,
                            viewsets)
from rest_framework.decorators import api_view  # Импортировали декоратор
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from .permissions import Admin, Moderator, Userr
from .serializers import (LoginSerializer, RegistrationSerializer,
                          UsersMeSerializer, UsersSerializer)

User = get_user_model()


class RegistrationAPIView(APIView):
    """
    Разрешить всем пользователям (аутентифицированным и нет) доступ к данному эндпоинту.
    """
    def post(self, request):
        data = request.data
        # username = data.get('username', None)
        # email = data.get('email', None)
        serializer = RegistrationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        username = serializer.data['username']
        pattern = r'^[\w.@+-]+\Z'
        if username == 'me' or not re.fullmatch(pattern, username):
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(username=username, email=email)
        except User.DoesNotExist:
            user = None
        if User.objects.filter(username=username, email=email).exists():
            confirmate_code = user.confirmate_code
            send_mail(
                subject='Code',
                message=f'confirmation code: {confirmate_code}',
                from_email='api@yamdb.not',
                recipient_list=[email],
                fail_silently=True,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            user = User.objects.create(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email']
            )
            user.save()
            confirmate_code = user.confirmate_code
            send_mail(
                subject='Code',
                message=f'confirmation code: {confirmate_code}',
                from_email='api@yamdb.not',
                recipient_list=[email],
                fail_silently=True,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)



    """ def post(self, request):
        data = request.data
        username = data.get('username', None)
        email = data.get('email', None)
        serializer = RegistrationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            pattern = r'^[\w.@+-]+\Z'
            if username == 'me' or not re.fullmatch(pattern, username):
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            user = User.objects.get(username=username)
            if user.email != email:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            confirmation_code = user.confirmate_code
            users_email = email
            send_mail(
                subject='Code',
                message=f'confirmation code: {confirmation_code}',
                from_email='api@yamdb.not',
                recipient_list=[users_email],
                fail_silently=True,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) """


class LoginViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    # model = User
    permission_classes = [AllowAny,]

    def create(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username',)
        confirmate_code = data.get('confirmate_code',)
        try:
            user = User.objects.get(username=username)
            if username and username == user.username and confirmate_code and confirmate_code == user.confrirmate_code:
                user.is_active = True
                if user.is_superuser:
                    user.role = 'admin'
                user.save()
                refresh = AccessToken.for_user(user)
                return Response(
                    {'acces': str(refresh), },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            raise ValidationError()


class UsersAPIView(APIView):

    def get(self, request):
        users = User.objects.all()
        serializer = UsersSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UsersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username',)
    permission_classes = (permissions.IsAuthenticated,)


class UsersMeAPIView(APIView):

    def get(self, request):
        user = User.objects.filter(username=request.user.username)
        serializer = UsersMeSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        # user = User.objects.get(username=self.request.user.username)
        # instance = User.objects.filter(username=self.request.user.username)
        serializer = UsersMeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class UsersMeViewSet(viewsets.ModelViewSet):
    serializer_class = UsersMeSerializer
    lookup_field = 'username'

    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)

    def perform_update(self, serializer):
        serializer.save(username=self.request.user.username)

class UsersMe(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    http_method_names = ['get', 'patch']
    lookup_field = 'username'
    serializer_class = UsersMeSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    http_method_names = ['get', 'patch', 'delete']
    # slug_field = 'username'
    lookup_field = 'username'
    serializer_class = UsersSerializer
    # permission_classes = (Admin,)
    permission_classes = (permissions.IsAdminUser,)
