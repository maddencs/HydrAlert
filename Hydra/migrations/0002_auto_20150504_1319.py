# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hydra', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensors',
            name='type',
            field=models.CharField(max_length=50, choices=[(b'ppm', b'PPM Sensor'), (b'pH', b'pH Sensor'), (b'temp', b'Temp/Humid Sensor'), (b'light', b'Light Sensor')]),
        ),
    ]
