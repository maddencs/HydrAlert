# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hydro', '0006_auto_20150420_1450'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alertemail',
            name='toaddrs',
        ),
    ]
