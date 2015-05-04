from django.contrib import admin
from Hydra.models import Sensors, PlotZone, Reservoir


admin.site.register(PlotZone)
admin.site.register(Reservoir)
admin.site.register(Sensors)