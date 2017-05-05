# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


def post_list(request):
    return render(request, 'index.html', {})

def search_form(request):
    return render(request, 'search_form.html')

def search(request):
    if 'q' in request.GET:
        message = 'You searched for: %r' % request.GET['q']
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)
