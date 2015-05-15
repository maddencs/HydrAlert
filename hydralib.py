import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HydrAlert.settings')

import django

django.setup()

from django.http import HttpResponse
from Hydra.models import Plot, Reservoir, AlertPlot, AlertRes, PlotHistory, ResHistory
from datetime import datetime
import smtplib, time

SERVER = smtplib.SMTP("smtp.gmail.com", 587)


# checks if current is within the fail limit of the goal. multiplies inputs by 10 for pH
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


# checks if the lights should be on right now
def light_check(plot_object, curr_time):
    start = plot_object.light_start
    end = plot_object.light_stop
    if start < curr_time < end:
        return True
    else:
        return False


# resets the alerts for an all plots and reservoirs related to the user
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


# checks alerts for plots or reservoirs and sets the relevant alerts while getting
# or creating an object with that type and setting those properties
def create_alert_object(obj_type, obj_id):
    time_now = datetime.now().time()
    if obj_type == 'plot':
        p = Plot.objects.get(pk=obj_id)
        if not light_check(p, time_now):
            p.light_alert = True
            pa = AlertPlot.objects.get_or_create(user=p.user, plot_id=p.id)[0]
            pa.lights = p.light_status
            p.save()
            pa.save()
        if not within_range(p.goal_temp, p.current_temp, p.temp_tolerance):
            p.temp_alert = True
            pa = AlertPlot.objects.get_or_create(user=p.user, plot_id=p.id)[0]
            pa.temp = p.temp
            pa.save()
            p.save()
    if obj_type == 'res':
        r = Reservoir.objects.get(pk=obj_id)
        if r.current_ph >= r.goal_ph_high and r.ph:
            r.ph_alert = True
            ra = AlertRes.objects.get_or_create(user=r.user, res_id=r.id)[0]
            ra.ph = r.ph
            ra.save()
            r.save()
        if r.current_ph <= r.goal_ph_low and r.ph:
            r.ph_alert = True
            ra = AlertRes.objects.get_or_create(user=r.user, res_id=r.id)[0]
            ra.ph = r.ph
            ra.save()
            r.save()
        if not within_range(r.goal_ppm, r.current_ppm, r.ppm_tolerance):
            r.ppm_alert = True
            ra = AlertRes.objects.get_or_create(user=r.user, res_id=r.id)[0]
            ra.ppm = r.ppm
            ra.save()
            r.save()


def make_history(**kwargs):
    obj_type = kwargs.pop('obj_type', None)
    obj_id = kwargs.pop('obj_id', None)
    data_type = kwargs.pop('data_type', None)
    date = str(datetime.now().date())
    if obj_type == 'plot':
        p = PlotHistory(date=date)
        p.plot = Plot.objects.get(pk=obj_id)
        p.save()
        if data_type == 'light_status' or data_type is None:
            p.light_status = Plot.objects.get(pk=obj_id).light_status
            p.save()
        if data_type == 'temp' or data_type is None:
            p.temp = Plot.objects.get(pk=obj_id).current_temp
            p.save()
        if data_type == 'humid' or data_type is None:
            p.humid = Plot.objects.get(pk=obj_id).current_humid
            p.save()
    if obj_type == 'res':
        r = ResHistory(date=date)
        r.res = Reservoir.objects.get(pk=obj_id)
        r.save()
        if data_type == 'ph' or data_type is None:
            r.ph = Reservoir.objects.get(pk=obj_id).current_ph
            r.save()
        if data_type == 'ppm' or data_type is None:
            r.ppm = Reservoir.objects.get(pk=obj_id).current_ppm
            r.save()