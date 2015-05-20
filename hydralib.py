import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HydrAlert.settings')

import django

django.setup()

from django.http import HttpResponse
from Hydra.models import Plot, Reservoir, AlertPlot, AlertRes, PlotHistory, ResHistory
from datetime import datetime, date
import smtplib
from django.contrib.auth.models import User

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


# makes history objects
def make_history(**kwargs):
    obj_type = kwargs.pop('obj_type', None)
    obj_id = kwargs.pop('obj_id', None)
    data_type = kwargs.pop('data_type', None)
    user_id = kwargs.pop('user', None)
    date = datetime.now().date()
    if obj_type in ('plot', None):
        plot_list = get_history('plot', obj_id, user_id)
        for plot in plot_list:
            p = PlotHistory(date=date)
            p.plot = plot
            if data_type in ('light_status', None):
                p.light_status = plot.light_status
                p.save()
            if data_type in ('temp', None):
                p.temp = plot.current_temp
                p.save()
            if data_type in ('humid', None):
                p.humid = plot.current_humid
                p.save()
    if obj_type in ('res', None):
        res_list = get_history('res', obj_id, user_id)
        for res in res_list:
            r = ResHistory(date=date)
            print(res)
            r.res = res
            if data_type == 'ph' or data_type is None:
                r.ph = res.current_ph
                r.save()
            if data_type == 'ppm' or data_type is None:
                r.ppm = res.current_ppm
                r.save()


# gets objects for making history used in make_history
def get_history(obj_type, obj_id, user_id):
    if obj_type == 'plot':
        if obj_id is None:
            return Plot.objects.filter(user__id=user_id)
        else:
            plot_list = []
            plot_list.append(Plot.objects.get(pk=obj_id))
            return plot_list
    elif obj_type == 'res':
        if obj_id is None:
            print(Reservoir.objects.filter(user__id=user_id))
            return Reservoir.objects.filter(user__id=user_id)
        else:
            res_list = []
            res_list.append(Reservoir.objects.get(pk=obj_id))
            return res_list


def make_alert(obj, property, value):
    # check obj's property 3 times with 5 minute intervals
    # if the alert object doesn't exist for this already then
    # create the alert object
    if property == 'ph':
        ar = AlertRes.objects.get_or_create(res=obj)[0]
        ar.ph = value
        ar.date = date.today()
        ar.time = datetime.now()
        ar.save()
    elif property == 'ppm':
        ar = AlertRes.objects.get_or_create(res=obj)[0]
        ar.ppm = value
        ar.date = date.today()
        ar.time = datetime.now()
        ar.save()
    elif property == 'lights':
        ap = AlertPlot.objects.get_or_create(plot=obj)[0]
        ap.lights = value
        ap.date = date.today()
        ap.time = datetime.now()
        ap.save()
    elif property == 'temp':
        ap = AlertPlot.objects.get_or_create(plot=obj)[0]
        ap.date = date.today()
        ap.time = datetime.now()
        ap.temp = value
        ap.save()
    elif property == 'humid':
        ap = AlertPlot.objects.get_or_create(plot=obj)[0]
        ap.date = date.today()
        ap.time = datetime.now()
        ap.humid = value
        ap.save()