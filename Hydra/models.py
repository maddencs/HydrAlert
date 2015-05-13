from django.db import models
from django.contrib.auth.models import User
from django import forms
from hydralib import within_range, light_check
from datetime import datetime

SENSOR_CHOICES = [('ppm', 'PPM Sensor'), ('pH', 'pH Sensor'), ('temp', 'Temp/Humid Sensor'), ('light', 'Light Sensor'), ]


class Plot(models.Model):
    user = models.ManyToManyField(User)
    name = models.CharField(max_length=40, blank=True)
    plot_comments = models.CharField(max_length=500, blank=True)
    current_temp = models.IntegerField(default=0)
    current_humid = models.IntegerField(default=0)
    light_start = models.TimeField(blank=True, null=True)
    light_stop = models.TimeField(blank=True, null=True)
    light_status = models.BooleanField(default=True)
    goal_temp = models.IntegerField(default=0)
    temp_tolerance = models.IntegerField(default=5)
    goal_humid = models.IntegerField(default=0)
    humid_alert = models.NullBooleanField(default=False)
    temp_alert = models.NullBooleanField(default=False)
    light_alert = models.NullBooleanField(default=False)
    alert_status = models.NullBooleanField(default=False)

    def check_stats(self):
        if not light_check(self, datetime.now().time()):
            self.light_alert = True
            self.light_status = False
        if not within_range(self.goal_temp, self.current_temp, self.temp_tolerance):
            self.temp_alert = True

    def check_alerts(self):
        if not self.temp_alert or not self.humid_alert or not self.light_alert:
            self.light_alert = True

    def __str__(self):
        return "Plot Zone " + str(self.id)


class Reservoir(models.Model):
    plot = models.ForeignKey(Plot)
    reservoir_comments = models.CharField(blank=True, max_length=300)
    current_ph = models.FloatField(default=0)
    current_ppm = models.IntegerField(default=0)
    res_change_date = models.DateField(default=None, null=True, blank=True)
    goal_ph_low = models.FloatField(default=5.5)
    goal_ph_high = models.FloatField(default=6.5)
    goal_ppm = models.IntegerField(default=0)
    ppm_tolerance = models.IntegerField(default=0)
    ph_alert = models.NullBooleanField(default=False)
    ppm_alert = models.NullBooleanField(default=False)
    res_change_alert = models.NullBooleanField(default=False)
    alert_status = models.NullBooleanField(default=False)

    def check_stats(self):
        if self.goal_ph_high < self.current_ph < self.goal_ph_low:
            self.ph_alert = True
        if not within_range(self.goal_ppm, self.current_ppm, self.ppm_tolerance):
            self.ppm_alert = True
        if self.res_change_date < datetime.datetime:
            self.res_change_alert = True

    def check_alerts(self):
        if not self.ph_alert or not self.ppm_alert or not self.res_change_alert:
            self.alert_status = True

    def __str__(self):
        return "Plot zone #" + str(self.plot.id) + "'s Reservoir #" + str(self.id)


class Sensors(models.Model):
    res = models.ForeignKey(Reservoir)
    type = models.CharField(max_length=50, choices=SENSOR_CHOICES)
    current_ph = models.FloatField(default=0)
    sensor_pin = models.CharField(default=None, max_length=10)

    def make_config(self):
        if self.type == 'pH':
            f = open('ph_config_' + str(self.res.id) + '.cfg', 'w')
            f.write(
                "void setup(){\n\tSerial.begin(9600)\n\t}\n\nvoid loop(){\n\tint sensorValue = analogRead(" +
                str(self.sensor_pin) + ");\n\tSerial.println(sensorValue);\n\tdelay(1000);\n\t}")
            f.close()
        elif self.type == 'temp':
            f = open('temp_config_' + str(self.res.id) + '.cfg', 'w')
            f.write("int val;\nint tempPin = " + self.sensor_pin + ";\n\nvoid setup(){\n\tSerial.begin(9600);\n}\n\nvoid loop()"
                                                              "\n\tval = analogRead(" + str(self.sensor_pin) + ");\n\tfloat mv ="
                                                              "(val/1024.0)*5000;\n\tfloat cel = mv/10;\n\tfloat farh - "
                                                              "(cel*9)/5 + 32;\n\nSerial.print('Temperature =');\nSerial."
                                                              "print(cel);\n\tSerial.print('*C');\nSerial.println();\n\t"
                                                              "delay(1000);\n\t}")
            f.close()


class AlertEmail(models.Model):
    user = models.ForeignKey(User)
    time_failed = models.DateTimeField()
    res = models.ForeignKey(Reservoir)
    plot_zone = models.ForeignKey(Plot)
    fromaddr = 'hydroponicsalert@gmail.com'
    toaddrs = models.EmailField(default=None)
    email_body = models.CharField(max_length=3000)
    sent = models.BooleanField(default=False)


class AlertPlot(models.Model):
    user = models.ForeignKey(User)
    plot_id = models.IntegerField(default=0)
    lights = models.NullBooleanField(default=False)
    temp = models.IntegerField(default=0)
    humid = models.IntegerField(default=0)


class AlertRes(models.Model):
    user = models.ForeignKey(User)
    res_id = models.IntegerField(default=0)
    ph = models.FloatField(default=0)
    ppm = models.IntegerField(default=0)


class PlotForm(forms.ModelForm):
    class Meta:
        model = Plot
        exclude = ('current_temp', 'lights_on', 'current_humid', 'user', 'humid_alert_sent', 'temp_alert_sent',
                   'light_alert_sent', )


class ReservoirForm(forms.ModelForm):
    class Meta:
        model = Reservoir
        fields = ['goal_ppm', 'goal_ph_low', 'goal_ph_high', 'ppm_tolerance']
        exclude = ('plot', 'current_ph', 'current_ppm', 'ph_alert_sent', 'ppm_alert_sent', 'res_change_alert',)