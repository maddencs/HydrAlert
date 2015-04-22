# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hydro', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensors',
            name='sensor_type',
            field=models.CharField(default=b'0', max_length=256, choices=[(b'0', b'Select Sensor Type'), (b'1', b'PPM Sensor'), (b'2', b'pH Sensor'), (b'3', b'Temp/Humid Sensor'), (b'4', b'Light Sensor')]),
        ),
        migrations.AlterField(
            model_name='plotzone',
            name='light_start',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='plotzone',
            name='light_stop',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='reservoir',
            name='reservoir_ph',
            field=models.FloatField(default=0),
        ),
    ]
