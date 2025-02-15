from django.shortcuts import render
from django.http import HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
from drf_yasg.utils import swagger_auto_schema  
from drf_yasg import openapi  


class LoginView(APIView):
    @swagger_auto_schema(
        operation_description="User logging and JWT token return", 
        request_body=LoginSerializer,  
        responses={200: openapi.Response('Logged', LoginSerializer)} 
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                'refresh': str(refresh),
                'access': access_token,
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
def test(request):
    return HttpResponse("Hey test")