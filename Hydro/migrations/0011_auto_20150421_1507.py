# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Hydro', '0010_auto_20150421_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='plotzone',
            name='light_start',
            field=models.TimeField(default=datetime.time(0, 0), verbose_name=b'%H%M'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plotzone',
            name='light_stop',
            field=models.TimeField(default=datetime.time(0, 0), verbose_name=b'%H%M'),
            preserve_default=False,
        ),
    ]
