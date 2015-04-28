import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HydroAlert.settings')

import django

django.setup()

from Hydro.models import AlertEmail, PlotZone, Reservoir
from datetime import datetime
from hydrolib import within_range, light_check, reset_alerts, send_email
from django.utils import timezone


USE_TZ = True


def check_stats():
    time_now = datetime.now().time()
    for plot in PlotZone.objects.all():
        reservoirs = Reservoir.objects.filter(plot=plot)
        for reservoir in reservoirs:
            ph = reservoir.current_ph
            temp = plot.current_temp
            goal_ph_low = reservoir.goal_ph_low
            goal_ph_high = reservoir.goal_ph_high
            goal_temp = plot.goal_temp
            if (ph <= goal_ph_low) and not reservoir.ph_alert_sent:
                email, created = AlertEmail.objects.get_or_create(plot_zone=plot,
                                                                  res=reservoir, time_failed=str(timezone.now()),
                                                                  msg="pH too low in Reservoir %s.")
                send_email(email)
                reservoir.ph_alert_sent = True
            elif ph >= goal_ph_high:
                    if not reservoir.ph_alert_sent:
                        email, created = AlertEmail.objects.get_or_create(plot_zone=plot,
                                                                          res=reservoir, time_failed=str(timezone.now())
                                                                          , msg="pH too high in Reservoir %s.")
                    send_email(email)
                    reservoir.ph_alert_sent = True
            elif not within_range(goal_temp, temp, 5):
                if not plot.temp_alert_sent:
                    email, created = AlertEmail.objects.get_or_create(plot_zone=plot,
                                                                      res=reservoir, time_failed=str(timezone.now()),
                                                                      msg="Temperature is currently %s which is 5 degrees"
                                                                          "out of range of your goal temp of %s")
                send_email(email)
                plot.temp_alert_sent = True

            elif not light_check(plot, time_now):
                email, created = AlertEmail.objects.get_or_create(plot_zone=plot,
                                                                  res=reservoir, time_failed=str(timezone.now()),
                                                                  msg="Temperature is currently %s which is 5 degrees "
                                                                      "out of range of your goal temp of %s")
                send_email(email)
                plot.light_alert_sent = True


if __name__ == '__main__':
    reset_alerts()