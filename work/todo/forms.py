from django import forms
from .models import Todo

class Task_form(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['details']
