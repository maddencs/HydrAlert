import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HydrAlert.settings')

import django

django.setup()

from django.http import HttpResponse
from django.shortcuts import render
from Hydra.models import PlotZone
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


def compile_alerts(user, email_plot_list, res_list):
    user = user
    plt_lst = email_plot_list
    res_list = res_list
    return render('Hydra/alert_email.html', user, res_list, plt_lst)


def make_config(**kwargs):
    type = kwargs.pop('type', None)
    sensor_pin = kwargs.pop('pin', '1')
    if type == 'pH':
        # add indentifier for res/plot in filename
        f = open('ph_config.cfg', 'w')
        f.write(
            "void setup(){\n\tSerial.begin(9600)\n\t}\n\nvoid loop(){\n\tint sensorValue = analogRead(" +
            str(sensor_pin) + ");\n\tSerial.println(sensorValue);\n\tdelay(1000);\n\t}")
        f.close()
    elif type == 'temp':
        f = open('temp_config.cfg', 'w')
        f.write("int val;\nint tempPin = " + sensor_pin + ";\n\nvoid setup(){\n\tSerial.begin(9600);\n}\n\nvoid loop()"
                                                          "\n\tval = analogRead(" + str(sensor_pin) + ");\n\tfloat mv ="
                                                          "(val/1024.0)*5000;\n\tfloat cel = mv/10;\n\tfloat farh - "
                                                          "(cel*9)/5 + 32;\n\nSerial.print('Temperature =');\nSerial."
                                                          "print(cel);\n\tSerial.print('*C');\nSerial.println();\n\t"
                                                          "delay(1000);\n\t}")


if __name__ == '__main__':
    make_config(type='pH', pin=2)
