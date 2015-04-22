# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hydro', '0003_auto_20150419_2035'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='UserProfile',
        ),
        migrations.RemoveField(
            model_name='plants',
            name='res_id',
        ),
        migrations.RemoveField(
            model_name='sensors',
            name='res_id',
        ),
        migrations.RemoveField(
            model_name='plotzone',
            name='PH_BOTTOM',
        ),
        migrations.RemoveField(
            model_name='plotzone',
            name='PH_TOP',
        ),
        migrations.AddField(
            model_name='plotzone',
            name='plot_comments',
            field=models.CharField(default='Blank Comment Field', max_length=3000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservoir',
            name='goal_ph_high',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='reservoir',
            name='goal_ph_low',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='reservoir',
            name='reservoir_comments',
            field=models.CharField(default='Blank Comment Field', max_length=3000),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Plants',
        ),
        migrations.DeleteModel(
            name='Sensors',
        ),
    ]
