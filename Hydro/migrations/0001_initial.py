# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plants',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlotZone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('PH_BOTTOM', models.FloatField(default=0)),
                ('PH_TOP', models.FloatField(default=0)),
                ('current_temp', models.IntegerField(default=0)),
                ('current_humid', models.IntegerField(default=0)),
                ('light_start', models.DateTimeField()),
                ('light_stop', models.DateTimeField()),
                ('goal_temp', models.IntegerField(default=0)),
                ('goal_humid', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Reservoir',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reservoir_ph', models.IntegerField(default=0)),
                ('reservoir_ppm', models.IntegerField(default=0)),
                ('res_change_date', models.DateTimeField()),
                ('plot_id', models.ForeignKey(to='Hydro.PlotZone')),
            ],
        ),
        migrations.CreateModel(
            name='Sensors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('res_id', models.ForeignKey(to='Hydro.Reservoir')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.AddField(
            model_name='plotzone',
            name='plot_owner',
            field=models.ForeignKey(to='Hydro.User'),
        ),
        migrations.AddField(
            model_name='plants',
            name='res_id',
            field=models.ForeignKey(to='Hydro.Reservoir'),
        ),
    ]
