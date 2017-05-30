from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from views import DictionaryView
from views import QuizView

urlpatterns = [
    url(r'^dictionary/?$', login_required(DictionaryView.as_view()), name='Translator'),
    url(r'^quiz/?$', login_required(QuizView.as_view()), name='Quiz'),
]
