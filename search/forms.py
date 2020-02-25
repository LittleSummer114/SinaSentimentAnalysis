#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms

class SearchForm(forms.Form):
    search_info = forms.CharField(label='Search Info', max_length=100)