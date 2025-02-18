from datetime import datetime
import pytz

from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import HydroponicSystem, Sensor
from .validators import validate_system_name, validate_activation_dt, validate_sensor_name, validate_read_dt


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError("Both fields are required.")

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid login or password.")
        
        attrs['user'] = user
        return attrs


class HydroponicSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = HydroponicSystem
        fields = '__all__'  
        read_only_fields = ['owner']  

    def validate_system_name(self, system_name):
        return validate_system_name(system_name)

    def validate_activation_dt(self, activation_dt):
        return validate_activation_dt(activation_dt)


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'
    
    def validate_sensor_name(self, sensor_name):
        return validate_sensor_name(sensor_name)

    def validate_read_dt(self, read_dt):
        return validate_read_dt(read_dt)