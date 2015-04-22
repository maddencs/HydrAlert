from django.db import models
from django import forms


TIME_FORMAT = '%H%M'
RES_PPM = 0
CHOICES = [('1', 'PPM Sensor'), ('2', 'pH Sensor'), ('3', 'Temp/Humid Sensor'),('4', 'Light Sensor'),]


class UserProfile(models.Model):
    name = models.CharField(max_length=25)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.name


class PlotZone(models.Model):
    plot_owner = models.ForeignKey(UserProfile)
    plot_comments = models.CharField(max_length=3000)
    plot_id = plot_owner.name
    current_temp = models.IntegerField(default=0)
    current_humid = models.IntegerField(default=0)
    light_start = models.TimeField(TIME_FORMAT)
    light_stop = models.TimeField(TIME_FORMAT)
    lights_on = None
    goal_temp = models.IntegerField(default=0)
    goal_humid = models.IntegerField(default=0)
    humid_alert_sent = False
    temp_alert_sent = False
    light_alert_sent = False

    def __str__(self):
        return str(self.plot_owner) + "'s Plot Zone " + str(self.id)


class Reservoir(models.Model):
    plot = models.ForeignKey(PlotZone)
    reservoir_comments = models.CharField(max_length=3000)
    current_ph = models.IntegerField(default=0)
    current_ppm = models.IntegerField(default=0)
    res_change_date = models.DateTimeField()
    goal_ph_low = models.IntegerField(default=0)
    goal_ph_high = models.IntegerField(default=0)
    ph_alert_sent = False
    ppm_alert_sent = False
    res_change_alert = False

    def __str__(self):
        return "Plot zone #" + str(self.plot.id) + "'s Reservoir #" + str(self.id)


class AlertEmail(models.Model):
    time_failed = models.DateTimeField()
    res = models.ForeignKey(Reservoir)
    plot_zone = models.ForeignKey(PlotZone)
    recipient = models.ForeignKey(UserProfile)
    fromaddr = 'hydroponicsalert@gmail.com'
    toaddrs = 'maddencs@gmail.com'
    msg = models.CharField(max_length=3000)
    sent = False