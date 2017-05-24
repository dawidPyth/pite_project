from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from views import DictionaryView, ProfileView, PasswordView

urlpatterns = [
    url(r'^dictionary/?$', login_required(DictionaryView.as_view()), name='Translator'),
    url(r'^change_email/?$', login_required(ProfileView.as_view()), name='Email_change'),
    url(r'^change_password/?$', login_required(PasswordView.as_view()), name='Password_change'),
]
