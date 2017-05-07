from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from views import DictionaryView

urlpatterns = [
    url(r'^dictionary/?$', login_required(DictionaryView.as_view()), name='Translator'),
]