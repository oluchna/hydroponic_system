import pytest
from rest_framework.exceptions import ValidationError
from datetime import datetime, timedelta
import pytz
from ..models import Sensor, HydroponicSystem, User
from ..serializers import SensorSerializer, HydroponicSystemSerializer
import uuid


@pytest.mark.django_db
class TestSensorSerializer:

    @pytest.fixture
    def user(self):
        """Fixture to create a User instance for the owner of the HydroponicSystem"""
        return User.objects.create_user(username="testuser", password="password123")

    @pytest.fixture
    def hydroponic_system(self, user):
        """Fixture to create a HydroponicSystem instance"""
        return HydroponicSystem.objects.create(
            system_name="Test Hydroponic System",
            volume=500.0,
            activation_dt=datetime.now(),
            num_of_chambers=4,
            owner=user
        )

    def test_valid_sensor_serializer(self, hydroponic_system):
        """Test that valid data is correctly serialized and deserialized"""

        valid_data = {
            "system_id": hydroponic_system.system_id,  
            "sensor_name": "Temperature Sensor",
            "value": 22.5,
            "read_dt": datetime.now(pytz.UTC)
        }

        serializer = SensorSerializer(data=valid_data)
        assert serializer.is_valid(), f"Serializer errors: {serializer.errors}"
        sensor = serializer.save()

        assert sensor.sensor_name == "Temperature Sensor"
        assert sensor.value == 22.5
        assert sensor.read_dt is not None

    def test_invalid_sensor_name_too_short(self, hydroponic_system):
        """Test validation when sensor_name is too short (less than 3 characters)"""
        invalid_data = {
            "system_id": hydroponic_system.system_id,
            "sensor_name": "A", 
            "value": 22.5,
            "read_dt": datetime.now(pytz.UTC)
        }

        serializer = SensorSerializer(data=invalid_data)
        assert not serializer.is_valid() 
        assert "sensor_name" in serializer.errors
        assert serializer.errors["sensor_name"][0] == "Sensor name field must consist of at least 3 characters."

    def test_invalid_read_dt_in_future(self, hydroponic_system):
        """Test validation when read_dt is in the future"""

        invalid_data = {
            "system_id": hydroponic_system.system_id,
            "sensor_name": "Humidity Sensor",
            "value": 45.0,
            "read_dt": datetime.now(pytz.UTC) + timedelta(days=1)
        }

        serializer = SensorSerializer(data=invalid_data)
        assert not serializer.is_valid() 
        assert "read_dt" in serializer.errors 
        assert serializer.errors["read_dt"][0] == "Sensor reading datetime cannot be from the future."

    def test_valid_read_dt(self, hydroponic_system):
        """Test that read_dt in the past or present is valid"""
        valid_data = {
            "system_id": hydroponic_system.system_id,
            "sensor_name": "Pressure Sensor",
            "value": 55.5,
            "read_dt": datetime.now(pytz.UTC)
        }

        serializer = SensorSerializer(data=valid_data)
        assert serializer.is_valid(), f"Serializer errors: {serializer.errors}"
        sensor = serializer.save()

        assert sensor.sensor_name == "Pressure Sensor"
        assert sensor.read_dt is not None


@pytest.mark.django_db
class TestHydroponicSystemSerializer:

    @pytest.fixture
    def user(self):
        """Fixture to create a User instance for the owner of the HydroponicSystem"""
        return User.objects.create_user(username="testuser", password="password123")

    @pytest.fixture
    def hydroponic_system(self):
        """Fixture to create a HydroponicSystem instance"""
        return {
            "system_id": uuid.uuid4(),
            "system_name": "Test System",
            "volume": 500.0,
            "activation_dt": datetime.now(pytz.UTC) - timedelta(days=1),
            "num_of_chambers": 4
        }

    def test_valid_hydroponic_system_serializer(self, hydroponic_system):
        """Test that valid data is correctly serialized and deserialized"""
        serializer = HydroponicSystemSerializer(data=hydroponic_system, context={"request": None})
        assert serializer.is_valid(), f"Serializer errors: {serializer.errors}"

    def test_invalid_system_name_too_short(user, hydroponic_system):
        """"""
        hydroponic_system["system_name"] = "A"
        serializer = HydroponicSystemSerializer(data=hydroponic_system)
        assert not serializer.is_valid()
        assert "system_name" in serializer.errors
        assert serializer.errors["system_name"][0] == "System name field must consist of at least 3 characters."

    def test_invalid_activation_dt_in_future(user, hydroponic_system):
        hydroponic_system["activation_dt"] = datetime.now(pytz.UTC) + timedelta(days=1)
        serializer = HydroponicSystemSerializer(data=hydroponic_system)
        assert not serializer.is_valid()
        assert "activation_dt" in serializer.errors
        assert serializer.errors["activation_dt"][0] == "Activation datetime cannot be from the future."