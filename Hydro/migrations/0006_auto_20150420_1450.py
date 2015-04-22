# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hydro', '0005_alertemail'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alertemail',
            old_name='plot',
            new_name='plot_zone',
        ),
        migrations.RenameField(
            model_name='reservoir',
            old_name='plot_id',
            new_name='plot',
        ),
    ]
