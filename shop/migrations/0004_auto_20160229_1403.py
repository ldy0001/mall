# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-29 06:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20160226_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_serial',
            field=models.IntegerField(max_length=32, unique=True),
        ),
    ]
