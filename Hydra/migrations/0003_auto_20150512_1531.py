# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hydra', '0002_auto_20150512_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alertplot',
            name='humid',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='alertplot',
            name='plot_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='alertplot',
            name='temp',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='alertres',
            name='ph',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='alertres',
            name='ppm',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='alertres',
            name='res_id',
            field=models.IntegerField(default=0),
        ),
    ]
