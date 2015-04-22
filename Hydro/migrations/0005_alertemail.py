# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hydro', '0004_auto_20150420_1232'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlertEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_failed', models.DateTimeField()),
                ('toaddrs', models.CharField(max_length=254)),
                ('msg', models.CharField(max_length=3000)),
                ('plot', models.ForeignKey(to='Hydro.PlotZone')),
                ('recipient', models.ForeignKey(to='Hydro.UserProfile')),
                ('res', models.ForeignKey(to='Hydro.Reservoir')),
            ],
        ),
    ]
