# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import DetailView
from random import randint
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

class QuizView(DetailView):

    def get(self, request):

        x = randint(4568, 9134)
        request.session['x'] = x 
        word_to_translate = []
	words_tuples = list(Words.objects.filter(id=x))
	word_to_translate = [the_tuple.word for the_tuple in words_tuples]
        
        context = {'print_word' : word_to_translate}
        return render(request, 'quiz.html', context)
        #return render(request, 'quiz.html', context={'quiz': ""})


    def post(self, request):
        translated_word = request.POST.get('word', "").lower()

        word = list(Words.objects.filter(word=translated_word))


        if 'x' in request.session:
            x = request.session['x']  
        else:
            x = 9001     

        count = 0
        if word:
            query_set = list(Translations.objects.filter(id_polish=word[0].id))
            ids = [int(word.id_eng) for word in query_set]
            print ids[0]

            if x == ids[0]:
                message = 'Correct!'
                count = count + 1
            else:
                message = 'Incorrect answer!'

        else:
            message = "Incorrect input"
        context = {'message' : message}
        return render(request, 'quiz.html', context)

