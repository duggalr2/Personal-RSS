# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-09-06 02:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_file', '0002_auto_20170831_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='feeds',
            name='category',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
