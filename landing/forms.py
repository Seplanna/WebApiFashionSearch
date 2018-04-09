from django import forms
from .models import *


class AssessorProfileForm(forms.ModelForm):

    class Meta:
        model = AssessorProfile
        exclude = [""]

