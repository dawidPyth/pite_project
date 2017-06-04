from django.conf.urls import url
from django.contrib.auth.decorators import login_required


from views import DictionaryView, ProfileView, PasswordView, QuizMainView
from views import DictionaryView, MixedQuiz, QuizSelection, Statistics, PolQuiz, EngQuiz
from views import SimpleQuizView

urlpatterns = [
    url(r'^dictionary/?$', login_required(DictionaryView.as_view()), name='Translator'),
    url(r'^change_email/?$', login_required(ProfileView.as_view()), name='Email_change'),
    url(r'^change_password/?$', login_required(PasswordView.as_view()), name='Password_change'),
    url(r'^quiz_main_page/?$', login_required(QuizMainView.as_view()), name='Quiz_main_page'),
    url(r'^quiz_selection/?$', login_required(QuizSelection.as_view()), name='QuizSelection'),
    url(r'^simplequiz/?$', login_required(SimpleQuizView.as_view()), name='SimpleQuiz'),
    url(r'^pol_quiz/?$', login_required(PolQuiz.as_view()), name='PolQuiz'),
    url(r'^eng_quiz/?$', login_required(EngQuiz.as_view()), name='EngQuiz'),
    url(r'^mixedquiz/?$', login_required(MixedQuiz.as_view()), name='MixedQuiz'),
    url(r'^statistics/?$', login_required(Statistics.as_view()), name='Statistics'),
]


