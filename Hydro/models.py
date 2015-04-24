from django.db import models
from django import forms
from datetimewidget.widgets import DateWidget

TIME_FORMAT = '%H%M'
RES_PPM = 0
CHOICES = [('1', 'PPM Sensor'), ('2', 'pH Sensor'), ('3', 'Temp/Humid Sensor'), ('4', 'Light Sensor'), ]


class PlotZone(models.Model):
    name = models.CharField(max_length=40, blank=True)
    plot_comments = models.CharField(max_length=3000, blank=True)
    current_temp = models.IntegerField(default=0)
    current_humid = models.IntegerField(default=0)
    light_start = models.TimeField(blank=True, null=False)
    light_stop = models.TimeField(blank=True, null=False)
    lights_on = None
    goal_temp = models.IntegerField(default=0)
    goal_humid = models.IntegerField(default=0)
    humid_alert_sent = False
    temp_alert_sent = False
    light_alert_sent = False

    def __str__(self):
        return "Plot Zone " + str(self.id)


class Reservoir(models.Model):
    plot = models.ForeignKey(PlotZone)
    reservoir_comments = models.CharField(max_length=3000)
    current_ph = models.IntegerField(default=0)
    current_ppm = models.IntegerField(default=0)
    res_change_date = models.DateField(default=None, null=False, blank=True)
    goal_ph_low = models.IntegerField(default=0)
    goal_ph_high = models.IntegerField(default=0)
    ph_alert_sent = models.NullBooleanField(default=False)
    ppm_alert_sent = models.NullBooleanField(default=False)
    res_change_alert = models.NullBooleanField(default=False)

    def __str__(self):
        return "Plot zone #" + str(self.plot.id) + "'s Reservoir #" + str(self.id)


class AlertEmail(models.Model):
    time_failed = models.DateTimeField()
    res = models.ForeignKey(Reservoir)
    plot_zone = models.ForeignKey(PlotZone)
    fromaddr = 'hydroponicsalert@gmail.com'
    toaddrs = 'maddencs@gmail.com'
    msg = models.CharField(max_length=3000)
    sent = models.BooleanField(default=False)


class ReservoirForm(forms.ModelForm):
    # res_change_date = forms.DateField(required=False, widget=DateWidget(usel10n=True, bootstrap_version=3))

    class Meta:
        model = Reservoir
        exclude = ('current_ph', 'current_ppm', 'plot', 'plot_id')
        widgets = {
            # Use localization and bootstrap 3
            'datetime': DateWidget(attrs={'id': "yourdatetimeid"}, usel10n=True, bootstrap_version=3)
        }


class PlotForm(forms.ModelForm):

    class Meta:
        model = PlotZone
        # fields = ('light_start', 'light_stop', 'goal_temp')
        exclude = ('current_temp', 'lights_on', 'current_humid', )


class Sensors(models.Model):

    type = models.CharField(max_length=50, choices=CHOICES)