# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-05-13 07:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CommentInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_id', models.IntegerField(unique=True)),
                ('comment_newsId', models.CharField(max_length=25, null=True)),
                ('comment_time', models.CharField(max_length=25, null=True)),
                ('comment_verify', models.IntegerField(default=0)),
                ('comment_nick', models.CharField(max_length=100, null=True)),
                ('comment_area', models.CharField(max_length=50, null=True)),
                ('comment_against', models.IntegerField(default=0)),
                ('comment_body', models.TextField(null=True)),
                ('preprocess', models.TextField(null=True)),
                ('postagging', models.TextField(null=True)),
                ('syntactic', models.TextField(null=True)),
                ('pv_word', models.TextField(null=True)),
                ('pv_modifierword', models.TextField(null=True)),
                ('keywords', models.TextField(null=True)),
                ('tag', models.IntegerField(default=-1)),
                ('sentiment', models.IntegerField(default=-1)),
                ('topic_id', models.IntegerField(default=-1)),
            ],
        ),
    ]