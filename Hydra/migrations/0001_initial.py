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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_failed', models.DateTimeField()),
                ('msg', models.CharField(max_length=3000)),
                ('sent', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PlotSensors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('port', models.CharField(max_length=20, null=True, blank=True)),
                ('type', models.CharField(max_length=50, choices=[(b'3', b'Temp/Humid Sensor'), (b'4', b'Light Sensor')])),
                ('light_status', models.NullBooleanField()),
                ('current_temp', models.IntegerField(default=0)),
                ('current_humid', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='PlotZone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40, blank=True)),
                ('plot_comments', models.CharField(max_length=500, blank=True)),
                ('current_temp', models.IntegerField(default=0)),
                ('current_humid', models.IntegerField(default=0)),
                ('light_start', models.TimeField(null=True, blank=True)),
                ('light_stop', models.TimeField(null=True, blank=True)),
                ('light_status', models.BooleanField(default=True)),
                ('goal_temp', models.IntegerField(default=0)),
                ('goal_humid', models.IntegerField(default=0)),
                ('humid_alert_sent', models.NullBooleanField(default=False)),
                ('temp_alert_sent', models.NullBooleanField(default=False)),
                ('light_alert_sent', models.NullBooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reservoir',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reservoir_comments', models.CharField(max_length=300, blank=True)),
                ('current_ph', models.FloatField(default=0)),
                ('current_ppm', models.IntegerField(default=0)),
                ('res_change_date', models.DateField(default=None, null=True, blank=True)),
                ('goal_ph_low', models.FloatField(default=5.5)),
                ('goal_ph_high', models.FloatField(default=6.5)),
                ('ph_alert_sent', models.NullBooleanField(default=False)),
                ('ppm_alert_sent', models.NullBooleanField(default=False)),
                ('res_change_alert', models.NullBooleanField(default=False)),
                ('plot', models.ForeignKey(to='Hydra.PlotZone')),
            ],
        ),
        migrations.CreateModel(
            name='ResSensors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('port', models.CharField(max_length=20, null=True, blank=True)),
                ('type', models.CharField(max_length=50, choices=[(b'1', b'PPM Sensor'), (b'2', b'pH Sensor')])),
                ('current_ph', models.FloatField()),
                ('current_ppm', models.FloatField()),
                ('res', models.ForeignKey(to='Hydra.Reservoir')),
            ],
        ),
        migrations.AddField(
            model_name='plotsensors',
            name='plot',
            field=models.ForeignKey(to='Hydra.PlotZone'),
        ),
        migrations.AddField(
            model_name='alertemail',
            name='plot_zone',
            field=models.ForeignKey(to='Hydra.PlotZone'),
        ),
        migrations.AddField(
            model_name='alertemail',
            name='res',
            field=models.ForeignKey(to='Hydra.Reservoir'),
        ),
    ]
