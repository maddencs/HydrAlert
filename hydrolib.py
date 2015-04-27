import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HydroAlert.settings')

import django

django.setup()

from django.http import HttpResponse
from Hydro.models import PlotZone, Reservoir
from datetime import datetime


def within_range(goal, current, fail_limit):
    # multiply by 10 because pH is a float
    goal = int(goal*10)
    current = int(current*10)
    fail_limit = int(fail_limit*10)
    lower_range = range((goal-fail_limit), goal+1)
    upper_range = range(goal, (goal+(fail_limit+1)))
    if (current in lower_range) or (current in upper_range):
        return True
    else:
        return False


def create_msg(**kwargs):
    email_template = kwargs.pop('email_template')
    context_dict = kwargs.pop('context_dict')
    return HttpResponse(email_template.render(context_dict))


def light_check(plot_object, curr_time):
    start = plot_object.light_start
    end = plot_object.light_stop
    if start < curr_time < end:
        return True
    else:
        return False


def reset_alerts():
    for Plot in PlotZone.objects.all():
        Plot.temp_alert_sent = False
        Plot.light_alert_sent = False
        Plot.humid_alert_sent = False
        Plot.save()
        for res in Plot.reservoir_set.all():
            res.ph_alert_sent = False
            res.ppm_alert_sent = False
            res.res_change_alert = False
            res.save()


if __name__ == '__main__':
    plot = PlotZone.objects.get(pk=1)
    plot.save()
    current_time = datetime.now().time()
    print light_check(plot, current_time)