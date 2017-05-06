# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect


def post_list(request):
    return render(request, 'index.html', {})


def search_form(request):
    return render(request, 'search_form.html')


def search(request):
    if request.method == 'GET':
        if 'q' in request.GET:
            message = 'You searched for: %r' % request.GET.get('q')
        else:
            message = 'You submitted an empty form.'

    if request.method == 'POST':
        if request.POST.get('message') is not None:
            return send_email(request)
        else:
            message = 'You submitted an empty form.'
    c = {'message': message}

    return render(request, 'searched.html', c)


def send_email(request):
    subject = 'Translation suggestion from user'
    message = request.POST.get('message')
    from_email = request.POST.get('from_email')
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, ['dawid.wk6@o2.pl'], fail_silently=False)
            HttpResponse('Email has been sent')

            return render(request, 'search_form.html')

            # msg = mail.EmailMessage(subject, message, to=['jan125djw@gmail.com'])
            # msg.send()
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
    return render(request, 'search_form.html')

# return HttpResponseRedirect('/search_form/')
# else:
#     return HttpResponse('Make sure all fields are entered and valid.')
