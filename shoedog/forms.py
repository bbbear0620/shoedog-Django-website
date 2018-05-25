from django import forms
from django.contrib import auth
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名',widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='密码',widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username,password=password)
        if user is None:
            raise forms.ValidationError('username or password error')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data



class RegisterForm(forms.Form):
    email = forms.CharField(label='email',
                            widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label='username',
                               max_length=30,
                               min_length=3,
                               widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='password',
                               min_length=6,
                               widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password_again = forms.CharField(label='password-again',
                                     min_length=6,
                                     widget=forms.PasswordInput(attrs={'class':'form-control'}))


    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('username is exist')
        return username
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('email is exist')
        return email
    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password_again != password:
            raise forms.ValidationError('password is not accordance')
        else:
            return password_again
