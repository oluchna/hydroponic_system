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
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView
from django_filters.rest_framework import DjangoFilterBackend



class HydroponicSystemPagination(PageNumberPagination):
    page_size = 3


class HydroponicSystemFilter(filters.FilterSet):
    system_name = filters.CharFilter(lookup_expr='icontains')
    volume = filters.RangeFilter()
    activation_dt = filters.DateTimeFromToRangeFilter()
    num_of_chambers = filters.RangeFilter()

    class Meta:
        model = HydroponicSystem
        fields = ['system_name', 'volume', 'activation_dt', 'num_of_chambers']


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

class HydroponicSystemView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]  
    serializer_class = HydroponicSystemSerializer

    queryset = HydroponicSystem.objects.all()  #
    filter_backends = (DjangoFilterBackend, OrderingFilter) 
    filterset_class = HydroponicSystemFilter 
    pagination_class = HydroponicSystemPagination 
    ordering_fields = ['system_name', 'volume', 'activation_dt', 'num_of_chambers'] 
    ordering = ['system_name']

    def get_queryset(self):
        return HydroponicSystem.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @swagger_auto_schema(
        operation_description="List of hydroponic systems with filters.",
        manual_parameters=[
            # Ordering parameter
            openapi.Parameter(
                'ordering',
                openapi.IN_QUERY,
                description="Field to order by. Can be system_name, volume, activation_dt, num_of_chambers",
                type=openapi.TYPE_STRING
            ),
            # system_name filter
            openapi.Parameter(
                'system_name',
                openapi.IN_QUERY,
                description="Filter by system name (case-insensitive).",
                type=openapi.TYPE_STRING
            ),
            # volume range filter
            openapi.Parameter(
                'volume_min',
                openapi.IN_QUERY,
                description="Filter by minimum volume.",
                type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'volume_max',
                openapi.IN_QUERY,
                description="Filter by maximum volume.",
                type=openapi.TYPE_NUMBER
            ),
            # activation_dt range filter
            openapi.Parameter(
                'activation_dt_from',
                openapi.IN_QUERY,
                description="Filter by minimum activation date (ISO 8601).",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'activation_dt_to',
                openapi.IN_QUERY,
                description="Filter by maximum activation date (ISO 8601).",
                type=openapi.TYPE_STRING
            ),
            # num_of_chambers range filter
            openapi.Parameter(
                'num_of_chambers_min',
                openapi.IN_QUERY,
                description="Filter by minimum number of chambers.",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'num_of_chambers_max',
                openapi.IN_QUERY,
                description="Filter by maximum number of chambers.",
                type=openapi.TYPE_INTEGER
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        systems = self.filter_queryset(self.get_queryset())
        systems = self.paginate_queryset(systems)
        serializer = self.get_serializer(systems, many=True)
        return self.get_paginated_response(serializer.data)




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
    


# class HydroponicSystemView(APIView):
#     permission_classes = [IsAuthenticated] 

#     serializer_class = HydroponicSystemSerializer
#     filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
#     filterset_class = HydroponicSystemFilter 
#     pagination_class = HydroponicSystemPagination
#     ordering_fields = ['system_name', 'volume', 'activation_dt', 'num_of_chambers']
#     ordering = ['system_name']

#     def get(self, request):
#         systems = HydroponicSystem.objects.filter(owner=request.user)
#         systems = self.filter_queryset(systems)
#         systems = self.order_queryset(systems)
#         paginator = self.pagination_class()
#         result_page = paginator.paginate_queryset(systems, request)
#         serializer = self.serializer_class(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     @swagger_auto_schema(
#     request_body=HydroponicSystemSerializer,  
#     responses={200: openapi.Response('New hydroponic system addition', HydroponicSystemSerializer)} 
#     )
#     def post(self, request):
#         data = request.data.copy() 
#         data['owner'] = request.user.id 
#         print(data['owner'])

#         serializer = HydroponicSystemSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save(owner=request.user) 
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

