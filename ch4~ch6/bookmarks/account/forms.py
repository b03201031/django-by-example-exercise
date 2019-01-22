from django import forms
from django.contrib.auth.models import User

from .models import Profile

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')



class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)


class userRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='repeat password', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email',)

    def clean_passwords(self):
        cd = self.cleaned_data

        if cd['password'] == cd['password2']:
            return cd['password2']
        else:
            raise forms.ValidationError('password not match')

