# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hydra', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='plotzone',
            name='alert_status',
            field=models.NullBooleanField(default=False),
        ),
    ]
