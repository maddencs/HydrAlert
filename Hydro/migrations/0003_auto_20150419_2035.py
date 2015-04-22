# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hydro', '0002_auto_20150419_1742'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservoir',
            old_name='reservoir_ph',
            new_name='current_ph',
        ),
        migrations.RenameField(
            model_name='reservoir',
            old_name='reservoir_ppm',
            new_name='current_ppm',
        ),
    ]
