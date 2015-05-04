from Hydra.models import Sensors

import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'HydrAlert.settings'

import django

django.setup()

if __name__ == '__main__':
    s = Sensors.objects.get(id=1)
    s.make_config()