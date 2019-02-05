# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-02-05 19:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FareSearch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userEmail', models.CharField(max_length=255)),
                ('userPhone', models.CharField(max_length=255)),
                ('originAirport', models.CharField(max_length=5)),
                ('destinationAirport', models.CharField(max_length=5)),
                ('departureDate', models.CharField(max_length=20)),
                ('returnDate', models.CharField(max_length=20)),
                ('lowestPrice', models.IntegerField(default=0)),
                ('averagePrice', models.IntegerField(default=0)),
            ],
        ),
    ]
