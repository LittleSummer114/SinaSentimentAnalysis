# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-06-16 11:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_auto_20160514_1747'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentinfo',
            name='mutisentiment',
            field=models.TextField(null=True),
        ),
    ]