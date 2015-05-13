# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hydra', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alertplot',
            name='alert_email',
        ),
        migrations.RemoveField(
            model_name='alertres',
            name='alert_email',
        ),
    ]
