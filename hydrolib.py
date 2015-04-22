import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HydroAlert.settings')

import django

django.setup()

from django.http import HttpResponse

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
    if start < curr_time:
        if curr_time < end:
            return True
        else:
            return False