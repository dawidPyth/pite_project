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
    if 'q' in request.GET:
        message = 'You searched for: %r' % request.GET['q']
    else:
        message = 'You submitted an empty form.'
    c = {'message': message}
    return render(request, 'searched.html', c)
    


def send_email(request):
    subject = 'translation suggestion from user'
    message = request.POST.get('message', '')
    from_email = request.POST.get('from_email', '')
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, ['jan125djw@gmail.com'], fail_silently=False)
	    HttpResponse('Email has been sent')
	    #msg = mail.EmailMessage(subject, message, to=['jan125djw@gmail.com'])
	    #msg.send()
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
	return render(request, 'search_form.thml')        
	#return HttpResponseRedirect('/search_form/')
    else:
        return HttpResponse('Make sure all fields are entered and valid.')




