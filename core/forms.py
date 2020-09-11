from django import forms
from .models import Question, Answer
from django.forms import DateInput


class AnswerCreateForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer']

