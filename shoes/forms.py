from django import forms
from .models import *

class ShoeDescriptionByAssessorForm(forms.ModelForm):

    class Meta:
        model = ShoeDescriptionByAssessor
        exclude = ["image_id", "user_profile"]

