from django.contrib.auth import (authenticate, get_user_model)
from django import forms

# If you don't do this you cannot use Bootstrap CSS

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(label="username")
    password = forms.CharField(widget=forms.PasswordInput, label="password")

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password")
            if not user.is_active:
                raise forms.ValidationError("User is inactive")
            return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email address')
    email2 = forms.EmailField(label='Confirm Email address')
    username = forms.CharField(label="username")
    password = forms.CharField(widget=forms.PasswordInput, label="password")

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'email2'
        ]

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            raise forms.ValidationError("Emails must match")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("Email exists")
        return super(UserRegisterForm,self).clean(*args, **kwargs)
