# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AlertEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('time_failed', models.DateTimeField()),
                ('toaddrs', models.EmailField(max_length=254, default=None)),
                ('email_body', models.CharField(max_length=3000)),
                ('sent', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='AlertPlot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('plot_id', models.IntegerField(default=None)),
                ('lights', models.NullBooleanField(default=False)),
                ('temp', models.IntegerField(default=None)),
                ('humid', models.IntegerField(default=None)),
                ('alert_email', models.ForeignKey(to='Hydra.AlertEmail')),
            ],
        ),
        migrations.CreateModel(
            name='AlertRes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('res_id', models.IntegerField(default=None)),
                ('ph', models.FloatField(default=None)),
                ('ppm', models.IntegerField(default=None)),
                ('alert_email', models.ForeignKey(to='Hydra.AlertEmail')),
            ],
        ),
        migrations.CreateModel(
            name='Plot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=40, blank=True)),
                ('plot_comments', models.CharField(max_length=500, blank=True)),
                ('current_temp', models.IntegerField(default=0)),
                ('current_humid', models.IntegerField(default=0)),
                ('light_start', models.TimeField(blank=True, null=True)),
                ('light_stop', models.TimeField(blank=True, null=True)),
                ('light_status', models.BooleanField(default=True)),
                ('goal_temp', models.IntegerField(default=0)),
                ('goal_humid', models.IntegerField(default=0)),
                ('humid_alert', models.NullBooleanField(default=False)),
                ('temp_alert', models.NullBooleanField(default=False)),
                ('light_alert', models.NullBooleanField(default=False)),
                ('alert_status', models.NullBooleanField(default=False)),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reservoir',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('reservoir_comments', models.CharField(max_length=300, blank=True)),
                ('current_ph', models.FloatField(default=0)),
                ('current_ppm', models.IntegerField(default=0)),
                ('res_change_date', models.DateField(blank=True, default=None, null=True)),
                ('goal_ph_low', models.FloatField(default=5.5)),
                ('goal_ph_high', models.FloatField(default=6.5)),
                ('goal_ppm', models.IntegerField(default=0)),
                ('ppm_tolerance', models.IntegerField(default=0)),
                ('ph_alert', models.NullBooleanField(default=False)),
                ('ppm_alert', models.NullBooleanField(default=False)),
                ('res_change_alert', models.NullBooleanField(default=False)),
                ('alert_status', models.NullBooleanField(default=False)),
                ('plot', models.ForeignKey(to='Hydra.Plot')),
            ],
        ),
        migrations.CreateModel(
            name='Sensors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('type', models.CharField(max_length=50, choices=[('ppm', 'PPM Sensor'), ('pH', 'pH Sensor'), ('temp', 'Temp/Humid Sensor'), ('light', 'Light Sensor')])),
                ('current_ph', models.FloatField(default=0)),
                ('sensor_pin', models.CharField(max_length=10, default=None)),
                ('res', models.ForeignKey(to='Hydra.Reservoir')),
            ],
        ),
        migrations.AddField(
            model_name='alertemail',
            name='plot_zone',
            field=models.ForeignKey(to='Hydra.Plot'),
        ),
        migrations.AddField(
            model_name='alertemail',
            name='res',
            field=models.ForeignKey(to='Hydra.Reservoir'),
        ),
        migrations.AddField(
            model_name='alertemail',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
