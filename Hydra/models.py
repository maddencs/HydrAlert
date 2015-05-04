from django.db import models
from django.contrib.auth.models import User

TIME_FORMAT = '%H%M'
RES_PPM = 0
PLOT_SENSOR_CHOICES = [('3', 'Temp/Humid Sensor'), ('4', 'Light Sensor'), ]
RES_SENSOR_CHOICES = [('1', 'PPM Sensor'), ('2', 'pH Sensor'), ]


class PlotZone(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=40, blank=True)
    plot_comments = models.CharField(max_length=500, blank=True)
    current_temp = models.IntegerField(default=0)
    current_humid = models.IntegerField(default=0)
    light_start = models.TimeField(blank=True, null=True)
    light_stop = models.TimeField(blank=True, null=True)
    light_status = models.BooleanField(default=True)
    goal_temp = models.IntegerField(default=0)
    goal_humid = models.IntegerField(default=0)
    humid_alert = models.NullBooleanField(default=False)
    temp_alert = models.NullBooleanField(default=False)
    light_alert = models.NullBooleanField(default=False)
    alert_status = models.NullBooleanField(default=False)

    def __str__(self):
        return "Plot Zone " + str(self.id)


class Reservoir(models.Model):
    plot = models.ForeignKey(PlotZone)
    reservoir_comments = models.CharField(blank=True, max_length=300)
    current_ph = models.FloatField(default=0)
    current_ppm = models.IntegerField(default=0)
    res_change_date = models.DateField(default=None, null=True, blank=True)
    goal_ph_low = models.FloatField(default=5.5)
    goal_ph_high = models.FloatField(default=6.5)
    ph_alert = models.NullBooleanField(default=False)
    ppm_alert = models.NullBooleanField(default=False)
    res_change_alert = models.NullBooleanField(default=False)
    alert_status = models.NullBooleanField(default=False)

    def __str__(self):
        return "Plot zone #" + str(self.plot.id) + "'s Reservoir #" + str(self.id)


class AlertEmail(models.Model):
    user = models.ForeignKey(User)
    time_failed = models.DateTimeField()
    res = models.ForeignKey(Reservoir)
    plot_zone = models.ForeignKey(PlotZone)
    fromaddr = 'hydroponicsalert@gmail.com'
    toaddrs = models.EmailField(default=None)
    msg = models.CharField(max_length=3000)
    sent = models.BooleanField(default=False)
    plt_alerts = []
    res_alerts = []


class PlotSensors(models.Model):
    plot = models.ForeignKey(PlotZone)
    port = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=50, choices=PLOT_SENSOR_CHOICES)
    light_status = models.NullBooleanField()
    current_temp = models.IntegerField(default=0)
    current_humid = models.IntegerField(default=0)


class ResSensors(models.Model):
    res = models.ForeignKey(Reservoir)
    port = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=50, choices=RES_SENSOR_CHOICES)
    current_ph = models.FloatField()
    current_ppm = models.FloatField()