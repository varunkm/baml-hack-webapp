# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-18 16:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stockhelper', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='StockQuote',
        ),
    ]
