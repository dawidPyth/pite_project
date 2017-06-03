from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (authenticate, get_user_model, login, logout)
from forms import UserLoginForm, UserRegisterForm
from django.contrib import messages
from django.views.generic import DetailView
from django import forms
from django.contrib.auth import (authenticate, get_user_model)
# Create your views here.
# this profile_app required decorator is to not allow to any
# view without authenticating


@login_required(login_url="profile_app/")
def home(request):
    # return render(request,"base.html")
    return render(request, "base.html")


class LoginView(DetailView):

    def post(self, request):
        logout(request)
        title = "Login"
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("/")
        else:
            messages.info(request, 'Wrong name or password!')
        return render(request, 'login.html', {"form": form, "title": title})

    def get(self, request):
        title = "Login"
        form = UserLoginForm(request.GET)
        return render(request, 'login.html', {"form": form, "title": title})


class LogoutView(DetailView):

    def post(self, request):
        logout(request)
        return render(request, 'logout.html', {})

    def get(self, request):
        logout(request)
        return render(request, 'logout.html', {})


class RegisterView(DetailView):

    def post(self, request):
        logout(request)
        title = 'Register'
        form = UserRegisterForm(request.POST or None)
        request.user.is_authenticated()
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password")
            user.set_password(password)
            user.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect("/")
        else:
            messages.info(request, form.errors)
        context = {
            "form": form,
            "title": title
        }
        return render(request, 'reg_form.html', context)

    def get(self, request):
        title = 'Register'
        form = UserRegisterForm(request.POST or None)
        context = {
            "form": form,
            "title": title
        }
        return render(request, 'reg_form.html', context)


User = get_user_model()
