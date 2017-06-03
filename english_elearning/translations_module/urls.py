from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from views import DictionaryView, MixedQuiz
from views import SimpleQuizView

urlpatterns = [
    url(r'^dictionary/?$', login_required(DictionaryView.as_view()), name='Translator'),
    url(r'^quiz/?$', login_required(SimpleQuizView.as_view()), name='SimpleQuiz'),
    url(r'^mixedquiz/?$', login_required(MixedQuiz.as_view()), name='MixedQuiz'),
]
