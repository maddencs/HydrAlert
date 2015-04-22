from django.db import models
from django import forms


TIME_FORMAT = '%H%M'
RES_PPM = 0
CHOICES = [('1', 'PPM Sensor'), ('2', 'pH Sensor'), ('3', 'Temp/Humid Sensor'), ('4', 'Light Sensor'), ]


class PlotZone(models.Model):
    plot_comments = models.CharField(max_length=3000)
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
    res_change_date = models.DateField(default=None, null=True)
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
    # recipient = models.ForeignKey(UserProfile)
    fromaddr = 'hydroponicsalert@gmail.com'
    toaddrs = 'maddencs@gmail.com'
    msg = models.CharField(max_length=3000)
    sent = False


class ReservoirForm(forms.ModelForm):
    # = Reservoir.plot
    # plot = forms.CharField(max_length=10, required=False)
    name = forms.CharField(max_length=128, help_text="Please enter a name to identify the reservoir.", )
    goal_ph_high = forms.IntegerField(max_value=14, min_value=0)
    goal_ph_low = forms.IntegerField(max_value=14, min_value=0, )
    temp_goal = forms.IntegerField(min_value=0, max_value=120, )
    # res_change_date = forms.DateField(required=False)

    class Meta:
        model = Reservoir
        exclude = ('current_ph', 'current_ppm', 'plot', 'res_change_date', 'plot_id')