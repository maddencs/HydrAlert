import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HydroAlert.settings')

import django

django.setup()

from Hydro.models import PlotZone, Reservoir
from django.core import serializers


def create_plots():
    plot1 = add_plot(light_start="08:00:00", light_stop="16:00:00", currenttemp=54, currenthumid=30, goaltemp=64,
                     goalhumid=35)

    add_reservoir(plot1, res_change_date="2011-11-15", currentph=7.2, goalphlow=7.0, goalphhigh=8.2)
    add_reservoir(plot1, res_change_date="2011-11-15", currentph=5.8, goalphlow= 5.0, goalphhigh=6.2)
    add_reservoir(plot1, res_change_date="2011-11-15", currentph=4.9, goalphlow= 4.0, goalphhigh=5.2)

    plot2 = add_plot(light_start="05:00:00", light_stop="20:00:00", currenttemp=38, currenthumid=54, goaltemp=94,
                     goalhumid=61)

    add_reservoir(plot2, res_change_date="2011-11-15", currentph=5.2, goalphlow= 5.0, goalphhigh=6.2)
    add_reservoir(plot2, res_change_date="2011-11-15", currentph=4.3, goalphlow= 4.0, goalphhigh=5.2)


def add_plot(light_start, light_stop, currenttemp, currenthumid, goaltemp, goalhumid):
    p = PlotZone.objects.get_or_create(light_start=light_start, light_stop=light_stop, current_temp=currenttemp, current_humid=currenthumid,
                 goal_temp=goaltemp, goal_humid=goalhumid)[0]
    p.save()
    return p


def add_reservoir(plot, res_change_date, currentph, goalphlow, goalphhigh):
    r = Reservoir.objects.get_or_create(plot=plot, res_change_date=res_change_date, current_ph=currentph, goal_ph_low=goalphlow,
                  goal_ph_high=goalphhigh)[0]
    r.save()
    return r

if __name__ == "__main__":
    create_plots()