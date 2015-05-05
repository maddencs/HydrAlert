import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HydrAlert.settings')

import django
django.setup()
from Hydra.models import Sensors

if __name__ == '__main__':
    print "get sensor"
    s = Sensors.objects.get(id=1)
    print s
    s.make_config()