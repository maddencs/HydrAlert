import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HydrAlert.settings')

import django

django.setup()

from django.contrib.auth.models import User
from Hydra.models import Plot, Reservoir
from hydralib import create_alert_object, make_history
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
        print("Work, dammit")
        try:
            for plot in Plot.objects.all():
                light_bool = random.randint(0, 100)
                if light_bool % 2 == 0:
                    light_status = False
                else:
                    light_status = True
                temp = random.randint(plot.current_temp-plot.temp_tolerance, plot.current_temp+plot.temp_tolerance)
                humid = random.randint(plot.current_humid-plot.humid_tolerance, plot.current_humid+plot.humid_tolerance)
                params = {'id': plot.id, 'temp': temp, 'humid': humid, 'lights': light_status, }
                print(light_status, light_bool)
                print("Plot ID: ", plot.id)
                pr = requests.post("http://localhost:8000/Hydra/update/plot/", data=params)
                # pr.prepare()
                print(pr.text)
        except TypeError:
            pass
        try:
            for res in Reservoir.objects.all():
                ph = '%.1f'%(random.uniform(res.goal_ph_low-1, res.goal_ph_high+1))
                ppm = random.randint(res.goal_ppm-50, res.goal_ppm+50)
                print(ppm)
                print("Reservoir: ", res.id)
                params2 = {'id': res.id, 'ph': ph, 'ppm': ppm, }
                rr = requests.post("http://localhost:8000/Hydra/update/reservoir/", data=params2)
                # rr.prepare()
                print(rr)
        except TypeError:
            pass

if __name__ == '__main__':
    change_stats()