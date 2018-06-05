from django import forms
from .models import *

class InterpretabilityForm(forms.ModelForm):
    class Meta:
        model = Interpretability
        exclude = ["iteration", "game_id", "method_id", "feature_n", "wright_answer", "given_answer"]