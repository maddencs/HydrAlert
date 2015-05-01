import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HydrAlert.settings')

import django

django.setup()

from Hydra.models import PlotZone, Reservoir
from django.contrib.auth.models import User


def check_stats():
    for user in User.objects.all():
        plot_alert_list = []
        res_alert_list = []
        for plot in PlotZone.objects.filter(user=user):
            reservoirs = Reservoir.objects.filter(plot=plot)
            plot.check_stats()
            if plot.alert_status:
                plot_alert_list.append(plot)
            for reservoir in reservoirs:
                reservoir.check_stats()
                if reservoir.alert_status:
                    res_alert_list.append(reservoir)
        """
        function to create email
        create template with alerts
        """

if __name__ == '__main__':
    check_stats()