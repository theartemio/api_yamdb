import random
import re
from http import HTTPStatus
from rest_framework.pagination import PageNumberPagination
from rest_framework import status, viewsets, permissions, generics, filters
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
# from .models import User
from django.contrib.auth import authenticate, get_user_model
from .permissions import Admin, Moderator, Userr

from .serializers import RegistrationSerializer, LoginSerializer, UsersSerializer, UsersMeSerializer

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
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
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
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


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
    # permission_classes = (permissions.IsAdminUser,)


class UsersMeAPIView(APIView):

    def get(self, request):
        user = User.objects.filter(username=request.user.username)
        serializer = UsersMeSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        # user = User.objects.get(username=self.request.user.username)
        serializer = UsersMeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class UsersMeViewSet(viewsets.ModelViewSet):
    serializer_class = UsersMeSerializer

    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)

    def perform_update(self, serializer):
        serializer.save(username=self.request.user.username)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    http_method_names = ['get', 'patch', 'delete']
    # slug_field = 'username'
    lookup_field = 'username'
    serializer_class = UsersSerializer
    # permission_classes = (Admin,)
    permission_classes = (permissions.IsAdminUser,)
