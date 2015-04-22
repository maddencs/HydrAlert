# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hydro', '0009_auto_20150421_1138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plotzone',
            name='light_start',
        ),
        migrations.RemoveField(
            model_name='plotzone',
            name='light_stop',
        ),
    ]
