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
	    word = request.GET.get('q')
            message = 'You searched for: %r' % word #request.GET.get('q')
        else:
            message = 'You submitted an empty form.'

    if request.method == 'POST':
        if request.POST.get('message') is not None:
            return send_email(request)
        else:
            message = 'You submitted an empty form.'
    c = {'message': message}
    request.session['word'] = word
    
    return render(request, 'searched.html', c)


def send_email(request):
    word = request.session['word']
    subject = "User suggestion of the word '{}'".format(word)
    message = "User suggested that the word '{}' could be translated as '{}'".format(word, request.POST.get('message'))
    from_email = request.POST.get('from_email')
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, ['jan125djw@gmail.com'], fail_silently=False)#['dawid.wk6@o2.pl']
            HttpResponse('Email has been sent')

            return render(request, 'search_form.html')

            # msg = mail.EmailMessage(subject, message, to=['jan125djw@gmail.com'])
            # msg.send()
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
    request.session.pop['mess', none]
    request.session.modified = True
    return render(request, 'search_form.html')

# return HttpResponseRedirect('/search_form/')
# else:
#     return HttpResponse('Make sure all fields are entered and valid.')
