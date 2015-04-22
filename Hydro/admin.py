from django.contrib import admin
from Hydro.models import PlotZone, Reservoir, UserProfile


class SensorsAdmin(admin.ModelAdmin):
    list_display = ('sensor_type', 'res_id')

admin.site.register(UserProfile)
admin.site.register(PlotZone)
admin.site.register(Reservoir)