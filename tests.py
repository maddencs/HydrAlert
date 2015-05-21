import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HydrAlert.settings')

import django

django.setup()

from django.contrib.auth.models import User
from Hydra.models import Plot, Reservoir
from hydralib import create_alert_object, make_history, make_alert
import requests
import random

# poorly named function that goes through checking stats of all the plots and reservoirs
# creates alert objects
def loop():
    for user in User.objects.all():
        for p in Plot.objects.filter(user=user):
            reservoirs = Reservoir.objects.filter(plot=p)
            create_alert_object('plot', p.id)
            for r in reservoirs:
                create_alert_object('res', r.id)


# Sends POST requests as actual objects would in order to update the db
def change_stats():
    while True:
        try:
            for plot in Plot.objects.all():
                light_bool = random.randint(0, 100)
                if light_bool % 2 == 0:
                    light_status = False
                else:
                    light_status = True
                temp = random.randint(plot.goal_temp-plot.temp_tolerance, plot.goal_temp+plot.temp_tolerance)
                humid = random.randint(plot.goal_humid-plot.humid_tolerance, plot.goal_humid+plot.humid_tolerance)
                params = {'id': plot.id, 'temp': temp, 'humid': humid, 'lights': light_status, }
                print(light_status, light_bool)
                pr = requests.post("http://52.11.95.35/Hydra/update/plot/", data=params)
                # pr.prepare()
        except TypeError:
            pass
        try:
            # for res in Reservoir.objects.all():
            i = 0;
            while i < 6:
                ph = '%.1f'%(random.uniform(4, 8))
                ppm = random.randint(800, 1000)
                params2 = {'id': i, 'ph': ph, 'ppm': ppm, }
                rr = requests.post("http://52.11.95.35//Hydra/update/reservoir/", data=params2)
                # rr.prepare()
                print(rr)
        except TypeError:
            pass

if __name__ == '__main__':
    change_stats()