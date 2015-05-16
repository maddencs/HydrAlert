import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HydrAlert.settings')

import django

django.setup()

from django.contrib.auth.models import User
from Hydra.models import Plot, Reservoir
from hydralib import create_alert_object, make_history
import datetime


# poorly named function that goes through checking stats of all the plots and reservoirs
# creates alert objects
def loop():
    for user in User.objects.all():
        for p in Plot.objects.filter(user=user):
            reservoirs = Reservoir.objects.filter(plot=p)
            create_alert_object('plot', p.id)
            for r in reservoirs:
                create_alert_object('res', r.id)


if __name__ == '__main__':
    make_history(user=1)