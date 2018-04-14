from django import forms
from shoes.forms import ShoeDescriptionByAssessorForm
from .models import *
from django.utils.safestring import mark_safe


class AnswerForm(forms.Form):

    CHOICES = [
                ('-2', "No difference"),
                ('0', '1st Column'),
               ('1', '2nd Column'),
               ('2', '3rd Column'),
               ('3', '4th Column'),
               ('4', '5th Column'),
               ('-1', "Don't know")]

    Answer_color = forms.ChoiceField(choices=CHOICES,
                               widget=forms.RadioSelect(
                                   )
                                 )
    Answer_shape = forms.ChoiceField(choices=CHOICES,
                               widget=forms.RadioSelect(
                                   )
                                 )



