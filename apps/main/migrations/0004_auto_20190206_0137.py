# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-06 01:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20190205_2234'),
    ]

    operations = [
        migrations.AddField(
            model_name='faresearch',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='faresearch',
            name='updatedAt',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
