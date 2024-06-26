from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, RegisterSerializer

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)

        if not serializer.is_valid():
            return Response(
                {
                    'success': False,
                    'message': 'Validation Error',
                    'data': serializer.errors,
                    'status': status.HTTP_400_BAD_REQUEST,
                    'code': 'bad request'
                },
                status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(
            {
                'success': True,
                'message': 'User Registered',
                'data': serializer.data,
                'status': status.HTTP_201_CREATED,
                'code': 'created'
            },
            status.HTTP_201_CREATED
        )


class LoginView(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response(
                {
                    'success': False,
                    'message': 'Validation Error',
                    'data': serializer.errors,
                    'status': status.HTTP_400_BAD_REQUEST,
                    'code': 'bad request'
                },
                status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=serializer.data['username'], password=serializer.data['password'])

        if not user:
            return Response(
                {
                    'success': False,
                    'message': 'Invalid Credentials',
                    'data': serializer.errors,
                    'status': status.HTTP_400_BAD_REQUEST,
                    'code': 'bad request'
                },
                status.HTTP_400_BAD_REQUEST
            )

        token, _ = Token.objects.get_or_create(user=user)

        response_data = serializer.data.copy()
        response_data["token"] = token.key

        return Response(
                {
                    'success': True,
                    'message': 'User logged in',
                    'data': response_data,
                    'status': status.HTTP_200_OK,
                    'code': 'ok'
                },
                status.HTTP_200_OK
            )
