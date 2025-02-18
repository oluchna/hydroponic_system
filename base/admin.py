from django.contrib import admin

from .models import HydroponicSystem, Sensor


admin.site.register(HydroponicSystem)
admin.site.register(Sensor)