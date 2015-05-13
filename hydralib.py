import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HydrAlert.settings')

import django

django.setup()

from django.http import HttpResponse
from django.shortcuts import render
from Hydra.models import Plot, AlertEmail
from datetime import datetime
import smtplib

SERVER = smtplib.SMTP("smtp.gmail.com", 587)


def within_range(goal, current, fail_limit):
    goal = int(goal * 10)
    current = int(current * 10)
    fail_limit = int(fail_limit * 10)
    lower_range = range((goal - fail_limit), goal + 1)
    upper_range = range(goal, (goal + (fail_limit + 1)))
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


def reset_alerts(request):
    for p in Plot.objects.filter(user=request.user):
        p.temp_alert_sent = False
        p.light_alert_sent = False
        p.humid_alert_sent = False
        p.save()
        for res in p.reservoir_set.all():
            res.ph_alert_sent = False
            res.ppm_alert_sent = False
            res.res_change_alert = False
            res.save()


def send_email(email):
    if not email.sent:
        msg = email.msg
        server = SERVER
        try:
            server.starttls()
            server.sendmail(email.fromaddr, email.toaddrs, msg)
            email.sent = True
        except smtplib.SMTPException:
            server.login('hydroponicsalert', 'HydroPass')
    else:
        pass


# def make_mail(user):
#     email_object = AlertEmail.objects.get_or_create(user=user, plot_alerts=plot_list, res_alerts=res_list)
#     email_object.save()
#     return render('Hydra/alert_email.html', user, res_list, plot_list)