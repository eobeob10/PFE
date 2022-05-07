from django import forms
from django.forms import ModelForm
from .models import Documents


class FileForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = ["name", "filepath"]
