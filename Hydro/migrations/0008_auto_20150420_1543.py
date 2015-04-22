# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hydro', '0007_remove_alertemail_toaddrs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservoir',
            name='current_ph',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='reservoir',
            name='goal_ph_high',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='reservoir',
            name='goal_ph_low',
            field=models.IntegerField(default=0),
        ),
    ]
