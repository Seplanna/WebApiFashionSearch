from django import forms
from shoes.forms import ShoeDescriptionByAssessorForm
from .models import *
from django.utils.safestring import mark_safe


class AnswerForm(forms.Form):

    CHOICES = [

                ('0', '1st Column'),
               ('1', '2nd Column'),
               ('2', '3rd Column'),
               ('3', '4th Column'),
               ('4', '5th Column')
    ]

    Answer = forms.ChoiceField(choices=CHOICES,
                               widget=forms.RadioSelect(
                                   )
                                 )

class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        exclude = ["task_id"]


class InterpretabilityForm(forms.ModelForm):
    class Meta:
        model = Interpretability
        exclude = ["iteration", "game_id"]