from django.test import TestCase
import pytest
from django.contrib.auth.models import User
from ..models import HydroponicSystem, Sensor
from django.core.exceptions import ValidationError
from datetime import datetime
import uuid
from django.utils import timezone


@pytest.mark.django_db
def test_create_hydroponic_system():
    '''The correctness of creating a hydroponic system.'''
    user = User.objects.create_user(username="testuser", password="password")
    system = HydroponicSystem.objects.create(
        system_name="Test System",
        volume=500.0,
        activation_dt=datetime.now(),
        num_of_chambers=4,
        owner=user
    )
    
    assert system.system_id is not None
    assert system.system_name == "Test System"
    assert system.volume == 500.0
    assert system.num_of_chambers == 4
    assert system.owner == user


@pytest.mark.django_db
def test_hydroponic_system_volume_validation():
    '''Testing that the volume does not take values below 0.'''
    user = User.objects.create_user(username="testuser", password="password")
    system = HydroponicSystem(
        system_name="Invalid Volume System",
        volume= -10.0,
        activation_dt=datetime.now(),
        num_of_chambers=3,
        owner=user
    )
    
    with pytest.raises(ValidationError):
        system.full_clean()


@pytest.mark.django_db
def test_hydroponic_system_num_of_chambers_validation():
    '''Testing that num_of_chambers does not take values above 100.'''
    user = User.objects.create_user(username="testuser", password="password")
    system = HydroponicSystem(
        system_name="Invalid Chambers System",
        volume=100.0,
        activation_dt=datetime.now(),
        num_of_chambers=150,
        owner=user
    )
    
    with pytest.raises(ValidationError):
        system.full_clean()

# @pytest.fixture
# def user():
#     """Fixture to create a User instance for the owner of the HydroponicSystem"""
#     return User.objects.create_user(username="testuser", password="password")


@pytest.fixture
def hydroponic_system():
        """Fixture to create a HydroponicSystem instance"""
        user = User.objects.create_user(username="testuser", password="password")
        return HydroponicSystem.objects.create(
            system_name="Test Hydroponic System",
            volume=500.0,
            activation_dt=timezone.now(),
            num_of_chambers=4,
            owner=user
        )


@pytest.mark.django_db
def test_create_sensor_reading(hydroponic_system):
    '''The correctness of creating a sensor reading.'''
    sensor = Sensor.objects.create(
            system_id=hydroponic_system,
            sensor_name="Temperature Sensor",
            value=25.5,
            read_dt=timezone.now()
    )
    
    assert sensor.sensor_name == "Temperature Sensor"
    assert sensor.value == 25.5
    assert sensor.system_id == hydroponic_system
    assert sensor.read_dt is not None


@pytest.mark.django_db
def test_sensor_name_length(hydroponic_system):
    '''Sensor name length test (more than 64 letters).'''
    sensor = Sensor(
            system_id=hydroponic_system,
            sensor_name="Sensor name longer than sixty four (64) letters testtttttttttttttttt.",
            value=25.5,
            read_dt=timezone.now()
    )
    
    with pytest.raises(ValidationError):
        sensor.full_clean()