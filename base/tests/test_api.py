import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from base.models import HydroponicSystem
from datetime import datetime, timedelta
import pytz
import uuid


@pytest.mark.django_db
class TestHydroponicSystemAPI:
    @pytest.fixture
    def user(self, db):
        return User.objects.create_user(username="testuser", password="password123")
    
    @pytest.fixture
    def user2(self, db):
        return User.objects.create_user(username="otheruser", password="password123")

    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def auth_client(self, api_client, user):
        api_client.force_authenticate(user=user)
        return api_client
    
    @pytest.fixture
    def hydroponic_systems(self, user, user2):
        return [
            HydroponicSystem.objects.create(
                system_name="System A", volume=500, activation_dt=datetime.now(pytz.UTC) - timedelta(days=10),
                num_of_chambers=5, owner=user
            ),
            HydroponicSystem.objects.create(
                system_name="System B", volume=700, activation_dt=datetime.now(pytz.UTC) - timedelta(days=5),
                num_of_chambers=3, owner=user
            ),
            HydroponicSystem.objects.create(
                system_name="Foreign System", volume=1000, activation_dt=datetime.now(pytz.UTC) - timedelta(days=20),
                num_of_chambers=10, owner=user2
            )
        ]

    def test_create_hydroponic_system(self, auth_client):
        data = {
            "system_id": uuid.uuid4(),
            "system_name": "Test System",
            "volume": 500.0,
            "activation_dt": (datetime.now(pytz.UTC) - timedelta(days=1)),
            "num_of_chambers": 4
        }
        response = auth_client.post("/systems/", data, format="json")

        assert response.status_code == 201  # Created
        assert response.data["system_name"] == "Test System"

    def test_get_hydroponic_systems(self, auth_client, hydroponic_systems):
        response = auth_client.get("/systems/")
        
        assert response.status_code == 200 
        assert len(response.data["results"]) == 2 
        system_names = [item["system_name"] for item in response.data["results"]]
        assert "System A" in system_names
        assert "System B" in system_names
        assert "Foreign System" not in system_names 


    def test_get_hydroponic_systems_with_filter(self, auth_client, hydroponic_systems):
        response = auth_client.get("/systems/", {"system_name": "System A"})
        
        assert response.status_code == 200
        assert len(response.data["results"]) == 1 
        assert response.data["results"][0]["system_name"] == "System A"

