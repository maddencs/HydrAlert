# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hydra', '0002_plotzone_alert_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservoir',
            name='alert_status',
            field=models.NullBooleanField(default=False),
        ),
    ]
