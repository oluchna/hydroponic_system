from drf_yasg.utils import swagger_auto_schema  

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from ..serializers import SensorSerializer


class SensorReadingView(APIView):
    """Sensor readings creation endpoint."""

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