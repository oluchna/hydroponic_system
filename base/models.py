from django.db import models
import uuid
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class HydroponicSystem(models.Model):
    system_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    system_name = models.CharField(max_length=64, null=False, blank=False)
    volume = models.FloatField()
    activation_date = models.DateTimeField()
    num_of_chambers = models.IntegerField(default=2, validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ])
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return f"System {self.system_name} owned by {self.owner}"


class Sensor(models.Model):
    system_id = models.ForeignKey(HydroponicSystem, on_delete=models.CASCADE, null=False, blank=False)
    sensor_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sensor_name =  models.CharField(max_length=64, null=False, blank=False)
    value = models.FloatField()
    read_ts = models.DateTimeField()

    def __str__(self):
        return f"Sensor {self.sensor_name} of system {self.system_id}"

