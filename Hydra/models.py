from django.db import models
from django.contrib.auth.models import User
SENSOR_CHOICES = [('ppm', 'PPM Sensor'), ('pH', 'pH Sensor'),
                  ('temp', 'Temp/Humid Sensor'), ('light', 'Light Sensor'), ]


class Plot(models.Model):
    user = models.ManyToManyField(User)
    name = models.CharField( max_length=40, blank=True)
    plot_comments = models.CharField(max_length=500, blank=True)
    current_temp = models.IntegerField(default=None, blank=True, null=True)
    current_humid = models.IntegerField(default=None, blank=True, null=True)
    light_start = models.TimeField(blank=True, null=True)
    light_stop = models.TimeField(blank=True, null=True)
    light_status = models.NullBooleanField(blank=True, null=True)
    goal_temp = models.IntegerField(default=None, blank=True, null=True)
    temp_tolerance = models.IntegerField(default=5)
    goal_humid = models.IntegerField(default=None, blank=True, null=True)
    humid_tolerance = models.IntegerField(default=5)
    humid_alert = models.NullBooleanField(default=False)
    temp_alert = models.NullBooleanField(default=False)
    light_alert = models.NullBooleanField(default=False)
    alert_status = models.NullBooleanField(default=False)

    def check_alerts(self):
        if not self.temp_alert or not self.humid_alert or not self.light_alert:
            self.alert_status = True
            return True
        else:
            return False

    def __str__(self):
        return "Plot Zone " + str(self.id)


class Reservoir(models.Model):
    plot = models.ForeignKey(Plot)
    user = models.ManyToManyField(User)
    reservoir_comments = models.CharField(blank=True, max_length=300)
    current_ph = models.FloatField(default=None, null=True, blank=True)
    current_ppm = models.IntegerField(default=None, null=True, blank=True)
    res_change_date = models.DateField(default=None, null=True, blank=True)
    goal_ph_low = models.FloatField(default=None, blank=True, null=True)
    goal_ph_high = models.FloatField(default=None, blank=True, null=True)
    goal_ppm = models.IntegerField(default=None, null=True, blank=True)
    ppm_tolerance = models.IntegerField(default=0)
    ph_alert = models.NullBooleanField(default=False)
    ppm_alert = models.NullBooleanField(default=False)
    res_change_alert = models.NullBooleanField(default=False)
    alert_status = models.NullBooleanField(default=False)

    def check_alerts(self):
        if not self.ph_alert or not self.ppm_alert or not self.res_change_alert:
            self.alert_status = True
            return True
        else:
            return False

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
    user = models.ForeignKey(User, null=True)
    time_failed = models.DateTimeField()
    res = models.ForeignKey(Reservoir)
    plot_zone = models.ForeignKey(Plot)
    fromaddr = 'hydroponicsalert@gmail.com'
    toaddrs = models.EmailField(default=None)
    email_body = models.CharField(max_length=3000)
    sent = models.BooleanField(default=False)


class AlertPlot(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    plot = models.ForeignKey(Plot)
    lights = models.NullBooleanField(null=True, blank=True)
    temp = models.IntegerField(default=None, null=True, blank=True)
    humid = models.IntegerField(default=None, null=True, blank=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(default=None, null=True, blank=True)


class AlertRes(models.Model):
    res = models.ForeignKey(Reservoir, null=True, blank=True)
    date = models.DateField(blank=True, null=True)
    ph = models.FloatField(default=None, null=True, blank=True)
    ppm = models.IntegerField(default=0, null=True, blank=True)
    time = models.TimeField(default=None, null=True, blank=True)


class PlotHistory(models.Model):
    plot = models.ForeignKey(Plot, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    light_status = models.NullBooleanField()
    temp = models.IntegerField(default=None, null=True, blank=True)
    humid = models.IntegerField(default=None,  null=True, blank=True)
    time = models.TimeField(default=None, null=True, blank=True)


class ResHistory(models.Model):
    res = models.ForeignKey(Reservoir, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    ph = models.IntegerField(default=None,  null=True, blank=True)
    ppm = models.IntegerField(default=None,  null=True, blank=True)