from django.contrib import admin
from Hydra.models import Sensors, Plot, Reservoir


admin.site.register(Plot)
admin.site.register(Reservoir)
admin.site.register(Sensors)