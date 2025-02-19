from drf_yasg.utils import swagger_auto_schema  
from drf_yasg import openapi  

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from ..serializers import HydroponicSystemSerializer, SensorSerializer
from ..models import HydroponicSystem, Sensor
from ..filters import HydroponicSystemFilter
from ..pagination import HydroponicSystemPagination


class HydroponicSystemView(ListCreateAPIView):
    """Enpoint for hydroponic system creation."""
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
        operation_description="Endpoint to get hydroponic systems with filters, ordering and pagination (3 elements per page).",
        manual_parameters=[
            openapi.Parameter(
                'ordering',
                openapi.IN_QUERY,
                description="Field to order by. Can be system_name, volume, activation_dt, num_of_chambers",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'system_name',
                openapi.IN_QUERY,
                description="Filter by system name (case-insensitive).",
                type=openapi.TYPE_STRING
            ),
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
            openapi.Parameter(
                'activation_dt_from',
                openapi.IN_QUERY,
                description="Filter by minimum activation date.",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'activation_dt_to',
                openapi.IN_QUERY,
                description="Filter by maximum activation date.",
                type=openapi.TYPE_STRING
            ),
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


class HydroponicSystemEdit(RetrieveUpdateDestroyAPIView):
    """
    Hydroponic system with given system_id endpoint.
    """
    permission_classes = [IsAuthenticated]
    queryset = HydroponicSystem.objects.all()
    serializer_class = HydroponicSystemSerializer
    lookup_field = "pk"

    @swagger_auto_schema(
        operation_description="Retrieve the details of the specified hydroponic system, including the last 10 sensor readings.",
        responses={200: HydroponicSystemSerializer()},
    )
    def get(self, request, *args, **kwargs):
        system_instance = self.get_object()
        sensors = Sensor.objects.filter(system_id=system_instance).order_by('-read_dt')[:10]
        sensor_serializer = SensorSerializer(sensors, many=True)
        system_serializer = self.get_serializer(system_instance)
        response_data = system_serializer.data
        response_data['last_sensors_readings'] = sensor_serializer.data
        return Response(response_data)

    @swagger_auto_schema(
        operation_description="Update the details of the specified hydroponic system.",
        request_body=HydroponicSystemSerializer,
        responses={200: HydroponicSystemSerializer()},
    )
    def put(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update the specified hydroponic system.",
        request_body=HydroponicSystemSerializer,
        responses={200: HydroponicSystemSerializer()},
    )
    def patch(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete the specified hydroponic system.",
        responses={204: 'No Content'},
    )
    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)