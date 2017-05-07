# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import DetailView

from models import Words, Translations


class DictionaryView(DetailView):

    def get(self, request):
        return render(request, 'dictionary.html', context={'translated_word': ""})

    def post(self, request):
        word_to_translate = request.POST.get('word', "").lower()
        translated_words = []
        word = list(Words.objects.filter(word=word_to_translate))

        if word:
            if word[0].language == "polish":
                query_set = list(Translations.objects.filter(id_polish=word[0].id))
                ids = [word.id_eng for word in query_set]
            else:
                query_set = list(Translations.objects.filter(id_eng=word[0].id))
                ids = [word.id_polish for word in query_set]

            results = list(Words.objects.filter(id__in=ids))
            translated_words = [translation.word for translation in results]

        else:
            translated_words.append("Word unknown!")

        context = {'translated_words': translated_words}
        return render(request, 'dictionary.html', context)