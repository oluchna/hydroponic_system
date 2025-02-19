from django.contrib import admin

from .models import HydroponicSystem, Sensor

"""Addition of read-only system_id field to admin panel"""
class HydroponicSystemAdmin(admin.ModelAdmin):
    readonly_fields = ('system_id',)


admin.site.register(HydroponicSystem, HydroponicSystemAdmin)
admin.site.register(Sensor)