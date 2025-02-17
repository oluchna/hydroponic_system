from django.shortcuts import render
from django.http import HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
from drf_yasg.utils import swagger_auto_schema  
from drf_yasg import openapi  
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import HydroponicSystemSerializer, SensorSerializer
from .models import HydroponicSystem, Sensor
from rest_framework.decorators import permission_classes
from rest_framework.generics import RetrieveUpdateDestroyAPIView




class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
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


class HydroponicSystemView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        systems = HydroponicSystem.objects.filter(owner=request.user)
        serializer = HydroponicSystemSerializer(systems, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
    request_body=HydroponicSystemSerializer,  
    responses={200: openapi.Response('New hydroponic system addition', HydroponicSystemSerializer)} 
    )
    def post(self, request):
        data = request.data.copy() 
        data['owner'] = request.user.id 
        print(data['owner'])

        serializer = HydroponicSystemSerializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=request.user) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SensorReadingView(APIView):
    permission_classes = [IsAuthenticated] 

    @swagger_auto_schema(
        request_body=SensorSerializer,
        responses={201: SensorSerializer, 400: "Invalid data"}
    )
    def post(self, request):
        serializer = SensorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HydroponicSystemEdit(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated] 

    queryset = HydroponicSystem.objects.all()
    serializer_class = HydroponicSystemSerializer
    lookup_field = "pk"

    def retrieve(self, request, *args, **kwargs):
        system_instance = self.get_object()
        sensors = Sensor.objects.filter(system_id=system_instance).order_by('-read_dt')[:10]
        sensor_serializer = SensorSerializer(sensors, many=True)
        system_serializer = self.get_serializer(system_instance)
        response_data = system_serializer.data
        response_data['last_sensors_readings'] = sensor_serializer.data

        return Response(response_data)