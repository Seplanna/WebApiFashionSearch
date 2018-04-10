from django import forms
from .models import *


class AssessorProfileForm(forms.ModelForm):

    class Meta:
        model = AssessorProfile
        exclude = ["login"]


class  LoginForm(forms.ModelForm):
    class Meta:
        model =  Login
        exclude = [""]