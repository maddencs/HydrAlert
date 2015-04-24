import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HydroAlert.settings')

import django

django.setup()

from Hydro.models import PlotZone, Reservoir, Sensors


def create_plots():
    Plot1 = add_plot(light_start="08:00:00", light_stop="16:00:00")

    add_reservoir(Plot1, res_change_date="2011-11-11")
    add_reservoir(Plot1, res_change_date="2011-11-12")
    add_reservoir(Plot1, res_change_date="2011-11-13")

    Plot2 = add_plot(light_start="05:00:00", light_stop="20:00:00")

    add_reservoir(Plot2, res_change_date="2011-11-14")
    add_reservoir(Plot2, res_change_date="2011-11-15")


def add_plot(light_start, light_stop):
    p = PlotZone.objects.get_or_create(light_start=light_start, light_stop=light_stop)[0]
    p.save()
    return p


def add_reservoir(plot, res_change_date):
    r = Reservoir.objects.get_or_create(plot=plot, res_change_date=res_change_date)[0]
    r.save()
    return r

if __name__ == "__main__":
    create_plots()