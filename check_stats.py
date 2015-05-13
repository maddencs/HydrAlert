import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HydrAlert.settings')

import django

django.setup()

from django.contrib.auth.models import User
from Hydra.models import Plot, Reservoir, AlertRes, AlertPlot
from datetime import datetime
from hydralib import within_range, light_check


def check_stats():
    time_now = datetime.now().time()
    for user in User.objects.all():
        for plot in Plot.objects.filter(user=user):
            reservoirs = Reservoir.objects.filter(plot=plot)
            plot.check_alerts()
            for reservoir in reservoirs:
                ph = reservoir.current_ph
                temp = plot.current_temp
                goal_ph_low = reservoir.goal_ph_low
                goal_ph_high = reservoir.goal_ph_high
                goal_temp = plot.goal_temp
                if ph <= goal_ph_low and ph != 0:
                    reservoir.ph_alert = True
                    alert_res = AlertRes.objects.get_or_create(user=user, res_id=reservoir.id)[0]
                    alert_res.ph = ph
                    alert_res.save()
                elif ph >= goal_ph_high and ph != 0:
                    reservoir.ph_alert = True
                    alert_res = AlertRes.objects.get_or_create(user=user, res_id=reservoir.id)[0]
                    alert_res.ph = ph
                    alert_res.save()
                elif not within_range(goal_temp, temp, 5):
                    plot.temp_alert = True
                    alert_plot = AlertPlot.objects.get_or_create(user=user, plot_id=plot.id)[0]
                    alert_plot.temp = temp
                    alert_plot.save()
                elif light_check(plot, time_now):
                    plot.light_alert = True
                    alert_plot = AlertPlot.objects.get_or_create(user=user, plot_id=plot.id)[0]
                    alert_plot.save()
                    alert_plot.lights = False


if __name__ == '__main__':
    check_stats()