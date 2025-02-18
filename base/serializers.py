from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import HydroponicSystem, Sensor
import re
from datetime import datetime
import pytz


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
        if len(system_name) < 3:
            raise serializers.ValidationError("System name field must consist of at least 3 characters.")
        return system_name

    def validate_activation_dt(self, activation_dt):
        now_utc = datetime.now(pytz.UTC)
        if activation_dt > now_utc:
            raise serializers.ValidationError("Activation datetime cannot be from the future.")
        return activation_dt


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'
    
    def validate_sensor_name(self, sensor_name):
        if len(sensor_name) < 3:
            raise serializers.ValidationError("Sensor name field must consist of at least 3 characters.")
        return sensor_name

    def validate_read_dt(self, read_dt):
        now_utc = datetime.now(pytz.UTC)
        if read_dt > now_utc:
            raise serializers.ValidationError("Sensor reading datetime cannot be from the future.")
        return read_dt