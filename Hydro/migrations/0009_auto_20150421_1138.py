# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hydro', '0008_auto_20150420_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plotzone',
            name='light_start',
            field=models.TimeField(verbose_name=b'%H%M'),
        ),
        migrations.AlterField(
            model_name='plotzone',
            name='light_stop',
            field=models.TimeField(verbose_name=b'%H%M'),
        ),
    ]
