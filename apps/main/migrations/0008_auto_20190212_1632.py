# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-12 16:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20190212_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='numFlights',
            field=models.IntegerField(default=0),
        ),
    ]
