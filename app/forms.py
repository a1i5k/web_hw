from django import forms
from django.core.exceptions import ValidationError
from django.forms import Textarea

from app.models import *


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterForm(forms.Form, forms.ModelForm):
    login = forms.CharField()
    email = forms.EmailField()
    nickname = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    repeat_password = forms.CharField(widget=forms.PasswordInput())

    def clean_email(self):
        email = self.cleaned_data['email']
        check = User.objects.filter(email=email).exists()
        if check:
            self.add_error(None, 'Email already exists')
        else:
            return email

    def clean_login(self):
        login = self.cleaned_data['login']
        check = User.objects.filter(username=login).exists()
        if check:
            self.add_error(None, 'Login already exists')
        else:
            return login

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        check = Profile.objects.filter(nickname=nickname).exists()
        if check:
            self.add_error(None, 'Email already exists')
        else:
            return nickname

    def clean(self):
        password = self.cleaned_data['password']
        repeat_password = self.cleaned_data['repeat_password']
        if password != repeat_password:
            self.add_error(None, 'Passwords does not math')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['login', 'email', 'nickname', 'password', 'repeat_password']


class SettingsForm(forms.Form, forms.ModelForm):
    login = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    nickname = forms.CharField(required=False)
    avatar = forms.ImageField(required=False)

    def clean_email(self):
        email = self.cleaned_data['email']
        check = User.objects.filter(email=email).exists()
        if email == '':
            return email
        elif check:
            self.add_error(None, 'Email already exists')
        else:
            return email

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        check = Profile.objects.filter(nickname=nickname).exists()
        if nickname == '':
            return nickname
        elif check:
            self.add_error(None, 'Nickname already exists')
        else:
            return nickname

    def clean_login(self):
        login = self.cleaned_data['login']
        check = User.objects.filter(username=login).exists()
        if check:
            self.add_error(None, 'Login already exists')
        else:
            return login

    class Meta:
        model = User
        fields = ['login', 'email', 'nickname', 'avatar']

    def save(self, *args, **kwarg):
        user = super().save(*args, **kwarg)
        if self.cleaned_data['avatar']:
            user.profile.avatar = self.cleaned_data['avatar']
        user.profile.save()
        return user


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'tag']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['body']

        widgets = {
            "body": Textarea(attrs={
                "class": "form-control input-text",
                "rows": "5"
            }
            )
        }
