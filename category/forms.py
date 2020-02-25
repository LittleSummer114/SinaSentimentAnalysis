#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms

class AddTopicForm(forms.Form):
    add_name_info = forms.CharField(label='Add Name Info', max_length=100)
    add_keywords_info = forms.CharField(label='Add Keywords Info', max_length=100)
    add_topic_type = forms.CharField(label='Add Topictype Info', max_length=100)