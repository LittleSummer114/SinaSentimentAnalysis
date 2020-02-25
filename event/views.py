#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

# 事件页面
def eventIndex(request):
    return render(request, 'event\\event.html')