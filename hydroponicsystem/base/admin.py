from django.contrib import admin

from .models import HydroponicSystem, Sensor


class HydroponicSystemAdmin(admin.ModelAdmin):
    readonly_fields = ('system_id',)


admin.site.register(HydroponicSystem, HydroponicSystemAdmin)
admin.site.register(Sensor)