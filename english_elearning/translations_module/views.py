# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import heapq

from django.shortcuts import render
from django.views.generic import DetailView
from random import randint
from models import Words, Translations, UserProgress, Quiz, QuizWords


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


class SimpleQuizView(DetailView):
    def get(self, request):

        x = randint(4568, 9134)
        request.session['x'] = x
        word_to_translate = []
        words_tuples = list(Words.objects.filter(id=x))
        word_to_translate = [the_tuple.word for the_tuple in words_tuples]

        context = {'print_word': word_to_translate}
        return render(request, 'quiz.html', context)
        # return render(request, 'quiz.html', context={'quiz': ""})

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
        context = {'message': message}
        return render(request, 'quiz.html', context)


class MixedQuiz(DetailView):
    def get(self, request):

        current_user_id = request.user.id

        # 14 words both languages
        words_per_language = 5
        pol_word_id_list = []
        eng_word_id_list = []
        known_word_id_list = []
        pol_words_list = []
        eng_words_list = []
        known_words_list = []

        # from already known words

        users_words = list(UserProgress.objects.filter(id_user=current_user_id))
        word_id_to_points = {'id_word': [], 'pol_points': [], 'eng_points': []}

        for single_word in users_words:
            word_id_to_points['id_word'].append(single_word.id_word)
            word_id_to_points['pol_points'].append(single_word.pol_points)
            word_id_to_points['eng_points'].append(single_word.eng_points)

        known_words_number_per_language = 2
        indexes_weak_words_eng = []
        indexes_weak_words_pol = []

        # take 3 words from pol and 3 from eng
        if word_id_to_points['id_word'].__len__() >= 3:
            weakest_words_points_eng = heapq.nsmallest(known_words_number_per_language,
                                                       word_id_to_points['eng_points'])
            weakest_words_points_pol = heapq.nsmallest(known_words_number_per_language,
                                                       word_id_to_points['pol_points'])

            for k in range(0, known_words_number_per_language):
                indexes_weak_words_eng += [i for i, word_position_eng in enumerate(word_id_to_points['eng_points']) if
                                           word_position_eng == weakest_words_points_eng[k]]
                indexes_weak_words_pol += [i for i, word_position_pol in enumerate(word_id_to_points['pol_points']) if
                                           word_position_pol == weakest_words_points_pol[k]]

            indexes_weak_words_eng = list(set(indexes_weak_words_eng))[:known_words_number_per_language]
            indexes_weak_words_pol = list(set(indexes_weak_words_pol))[:known_words_number_per_language]

            for o in range(0, known_words_number_per_language):
                known_word_id_list.append(word_id_to_points['id_word'][indexes_weak_words_eng[o]])
                known_word_id_list.append(word_id_to_points['id_word'][indexes_weak_words_pol[o]])

            for i in range(0, known_word_id_list.__len__()):
                known_words_list.append(Words.objects.filter(id=known_word_id_list[i])[0].word)
        else:
            for i in range(0, known_words_number_per_language * 2):
                known_word_id_list.append(randint(1, 9134))
                known_words_list.append(Words.objects.filter(id=known_word_id_list[i])[0].word)

        # from all words
        for i in range(0, words_per_language):
            pol_word_id_list.append(randint(1, 4567))
            pol_words_list.append(Words.objects.filter(id=pol_word_id_list[i])[0].word)

            eng_word_id_list.append(randint(4568, 9134))
            eng_words_list.append(Words.objects.filter(id=eng_word_id_list[i])[0].word)

        words_list = pol_words_list + eng_words_list + known_words_list
        words_list_id = pol_word_id_list + eng_word_id_list + known_word_id_list
        context = {'words_list_id': words_list_id, 'words_list': words_list}

        return render(request, 'mixed_quiz.html', context=context)

    def post(self, request):

        current_user_id = request.user.id
        user_words = []
        original_words = []
        original_words_id = []
        words_number = 14
        good_answers = 0
        for i in range(1, words_number+1):
            current_word = request.POST.get('word{0}'.format(i), "").lower()
            user_words.append(current_word)

            current_original_word = request.POST.get('original_word{0}'.format(i), "").lower()
            original_words.append(current_original_word)

            current_original_word_id = request.POST.get('original_word_id{0}'.format(i), "")
            original_words_id.append(current_original_word_id)

            original_word = list(Words.objects.filter(id=current_original_word_id))
            word = list(Words.objects.filter(word=current_word))
            original_word_language = original_word[0].language

            if word:

                word_language = word[0].language
                if word_language == "polish":
                    query_set = list(Translations.objects.filter(id_polish=word[0].id))
                    translated_id = [word.id_eng for word in query_set]
                else:
                    query_set = list(Translations.objects.filter(id_eng=word[0].id))
                    translated_id = [word.id_polish for word in query_set]

                if translated_id[0] == int(original_words_id[i - 1]):
                    # dodaje punkty do slowa bo odpowiedzial poprawnie
                    # patrzymy czy istnieje
                    try:
                        answer = UserProgress.objects.get(id_user=current_user_id,
                                                          id_word=int(original_words_id[i - 1]))
                        if original_word_language == "polish":
                            answer.pol_points += 10
                            answer.status = "passed"
                        else:
                            answer.eng_points += 10
                            answer.status = "passed"
                        answer.save()
                    except UserProgress.DoesNotExist:
                        # tworzymy nowy wpis
                        if original_word_language == "polish":
                            answer = UserProgress(id_user=current_user_id, id_word=int(original_words_id[i - 1]),
                                                  status="passed", pol_points=10, eng_points=0)
                        else:
                            answer = UserProgress(id_user=current_user_id, id_word=int(original_words_id[i - 1]),
                                                  status="passed", pol_points=0, eng_points=10)
                        answer.save()
                    good_answers += 1

            else:
                # slowa nie ma w slowniku wiec niepoprawna odpowiedz
                # patrzymy czy istnieje juz wpis
                try:
                    bad_answer = UserProgress.objects.get(id_user=current_user_id,
                                                          id_word=int(original_words_id[i - 1]))

                    if original_word_language == "polish":
                        bad_answer.pol_points -= 10
                        bad_answer.status = "failed"
                    else:
                        bad_answer.eng_points -= 10
                        bad_answer.status = "failed"
                    bad_answer.save()
                except UserProgress.DoesNotExist:
                    # tworzymy nowy wpis
                    if original_word_language == "polish":
                        bad_answer = UserProgress(id_user=current_user_id, id_word=int(original_words_id[i - 1]),
                                                  status="failed", pol_points=-10, eng_points=0)
                    else:
                        bad_answer = UserProgress(id_user=current_user_id, id_word=int(original_words_id[i - 1]),
                                                  status="failed", pol_points=0, eng_points=-10)
                    bad_answer.save()

        result = "%.2f" % (float(good_answers) / original_words_id.__len__() * 100)
        quiz_result = Quiz(id_user=current_user_id, result=result,
                           quiz_type_id=1)
        quiz_result.save()

        id_quiz = Quiz.objects.latest('id').id
        for id in original_words_id:
            quiz_words = QuizWords(id_quiz=id_quiz, id_word=id)
            quiz_words.save()
        context = {'result': result}
        return render(request, 'results.html', context=context)


class PolQuiz(DetailView):
    def get(self, request, *args, **kwargs):
        word_number = 10
        pol_word_id_list = []
        pol_words_list = []
        # from all words
        for i in range(0, word_number):
            pol_word_id_list.append(randint(1, 4567))
            pol_words_list.append(Words.objects.filter(id=pol_word_id_list[i])[0].word)

        context = {'pol_word_id_list': pol_word_id_list, 'pol_words_list': pol_words_list}

        return render(request, 'pol_quiz.html', context=context)

    def post(self, request):

        current_user_id = request.user.id
        user_words = []
        original_words = []
        original_words_id = []
        words_number = 10
        good_answers = 0
        for i in range(1, words_number+1):
            current_word = request.POST.get('word{0}'.format(i), "").lower()
            user_words.append(current_word)

            current_original_word = request.POST.get('original_word{0}'.format(i), "").lower()
            original_words.append(current_original_word)

            current_original_word_id = request.POST.get('original_word_id{0}'.format(i), "")
            original_words_id.append(current_original_word_id)

            original_word = list(Words.objects.filter(id=current_original_word_id))
            word = list(Words.objects.filter(word=current_word))
            original_word_language = original_word[0].language

            if word:

                word_language = word[0].language
                if word_language == "polish":
                    query_set = list(Translations.objects.filter(id_polish=word[0].id))
                    translated_id = [word.id_eng for word in query_set]
                else:
                    query_set = list(Translations.objects.filter(id_eng=word[0].id))
                    translated_id = [word.id_polish for word in query_set]

                if translated_id[0] == int(original_words_id[i - 1]):
                    # dodaje punkty do slowa bo odpowiedzial poprawnie
                    # patrzymy czy istnieje
                    try:
                        answer = UserProgress.objects.get(id_user=current_user_id,
                                                          id_word=int(original_words_id[i - 1]))
                        answer.pol_points += 10
                        answer.status = "passed"
                        answer.save()
                    except UserProgress.DoesNotExist:
                        # tworzymy nowy wpis
                        answer = UserProgress(id_user=current_user_id, id_word=int(original_words_id[i - 1]),
                                              status="passed", pol_points=10, eng_points=0)
                        answer.save()
                    good_answers += 1

            else:
                # slowa nie ma w slowniku wiec niepoprawna odpowiedz
                # patrzymy czy istnieje juz wpis
                try:
                    bad_answer = UserProgress.objects.get(id_user=current_user_id,
                                                          id_word=int(original_words_id[i - 1]))
                    bad_answer.pol_points -= 10
                    bad_answer.status = "failed"
                    bad_answer.save()
                except UserProgress.DoesNotExist:
                    # tworzymy nowy wpis

                    bad_answer = UserProgress(id_user=current_user_id, id_word=int(original_words_id[i - 1]),
                                              status="failed", pol_points=-10, eng_points=0)
                    bad_answer.save()

        result = "%.2f" % (float(good_answers) / original_words_id.__len__() * 100)
        quiz_result = Quiz(id_user=current_user_id, result=result,
                           quiz_type_id=2)
        quiz_result.save()

        id_quiz = Quiz.objects.latest('id').id
        for id in original_words_id:
            quiz_words = QuizWords(id_quiz=id_quiz, id_word=id)
            quiz_words.save()
        context = {'result': result}
        return render(request, 'results.html', context=context)


class EngQuiz(DetailView):
    def get(self, request, *args, **kwargs):
        word_number = 10
        eng_word_id_list = []
        eng_words_list = []
        # from all words
        for i in range(0, word_number):
            eng_word_id_list.append(randint(4568, 9134))
            eng_words_list.append(Words.objects.filter(id=eng_word_id_list[i])[0].word)

        context = {'eng_word_id_list': eng_word_id_list, 'eng_words_list': eng_words_list}

        return render(request, 'eng_quiz.html', context=context)

    def post(self, request):

        current_user_id = request.user.id
        user_words = []
        original_words = []
        original_words_id = []
        words_number = 10
        good_answers = 0
        for i in range(1, words_number+1):
            current_word = request.POST.get('word{0}'.format(i), "").lower()
            user_words.append(current_word)

            current_original_word = request.POST.get('original_word{0}'.format(i), "").lower()
            original_words.append(current_original_word)

            current_original_word_id = request.POST.get('original_word_id{0}'.format(i), "")
            original_words_id.append(current_original_word_id)

            original_word = list(Words.objects.filter(id=current_original_word_id))
            word = list(Words.objects.filter(word=current_word))
            original_word_language = original_word[0].language

            if word:

                word_language = word[0].language
                if word_language == "polish":
                    query_set = list(Translations.objects.filter(id_polish=word[0].id))
                    translated_id = [word.id_eng for word in query_set]
                else:
                    query_set = list(Translations.objects.filter(id_eng=word[0].id))
                    translated_id = [word.id_polish for word in query_set]

                if translated_id[0] == int(original_words_id[i - 1]):
                    # dodaje punkty do slowa bo odpowiedzial poprawnie
                    # patrzymy czy istnieje
                    try:
                        answer = UserProgress.objects.get(id_user=current_user_id,
                                                          id_word=int(original_words_id[i - 1]))
                        answer.eng_points += 10
                        answer.status = "passed"
                        answer.save()
                    except UserProgress.DoesNotExist:
                        # tworzymy nowy wpis

                        answer = UserProgress(id_user=current_user_id, id_word=int(original_words_id[i - 1]),
                                              status="passed", pol_points=0, eng_points=10)
                        answer.save()
                    good_answers += 1

            else:
                # slowa nie ma w slowniku wiec niepoprawna odpowiedz
                # patrzymy czy istnieje juz wpis
                try:
                    bad_answer = UserProgress.objects.get(id_user=current_user_id,
                                                          id_word=int(original_words_id[i - 1]))

                    bad_answer.eng_points -= 10
                    bad_answer.status = "failed"
                    bad_answer.save()
                except UserProgress.DoesNotExist:
                    # tworzymy nowy wpis

                    bad_answer = UserProgress(id_user=current_user_id, id_word=int(original_words_id[i - 1]),
                                              status="failed", pol_points=0, eng_points=-10)
                    bad_answer.save()

        result = "%.2f" % (float(good_answers) / original_words_id.__len__() * 100)
        quiz_result = Quiz(id_user=current_user_id, result=result,
                           quiz_type_id=3)
        quiz_result.save()

        id_quiz = Quiz.objects.latest('id').id
        for id in original_words_id:
            quiz_words = QuizWords(id_quiz=id_quiz, id_word=id)
            quiz_words.save()
        context = {'result': result}
        return render(request, 'results.html', context=context)


class QuizSelection(DetailView):
    def get(self, request):
        return render(request, 'quiz_selection.html')


class Statistics(DetailView):
    def get(self, request):
        return render(request, 'statistics.html')
