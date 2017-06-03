# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.contrib.auth import (authenticate, get_user_model)
from django.contrib import messages
from models import Words, Translations
from forms import ChangeEmail, ChangePassword

User = get_user_model()


class DictionaryView(DetailView):

    def get(self, request):
        return render(request, 'dictionary.html', context={'translated_word': ""})

    def post(self, request):
        word_to_translate = request.POST.get('word', "").lower()
        translated_words = []
        word = list(Words.objects.filter(word=word_to_translate))
        language = word[0].language
        if word:
            if language == "polish":
                query_set = list(Translations.objects.filter(id_polish=word[0].id))
                ids = [word.id_eng for word in query_set]
            else:
                query_set = list(Translations.objects.filter(id_eng=word[0].id))
                ids = [word.id_polish for word in query_set]

            results = list(Words.objects.filter(id__in=ids))
            translated_words = [translation.word for translation in results]

        else:
            translated_words.append("Word unknown!")

        context = {'translated_words': translated_words, 'word_to_translate': word_to_translate , 'language': language}
        return render(request, 'dictionary.html', context)


class ProfileView(DetailView):

    def get(self, request):
        return render(request, 'change_email.html')

    def post(self, request):
        email = request.POST.get('email')
        email2 = request.POST.get('email2')
        user = request.user
        if (email == email2) and email:
            user.email = email
            user.save()
            messages.success(request, 'Profile details updated.')
        elif not email:
            messages.info(request, 'Provide emails')
        else:
            messages.error(request, 'Emails doesn\'t match')
        return render(request, 'change_email.html')


class PasswordView(DetailView):

    def get(self, request):
        return render(request, 'change_password.html')

    def post(self, request):
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        user = request.user
        if password == password2 and password:
            user.set_password(password)
            user.save()
            messages.success(request, 'Profile details updated.')
        elif not password:
            messages.info(request, 'Provide passwords')
        else:
            messages.error(request, 'Passwords doesn\'t match')
        return render(request, 'change_password.html')


class QuizMainView(DetailView):

    def get(self, request):
        return render(request, 'quiz_main_page.html')

    def post(self, request):
        return render(request, 'quiz_main_page.html')
