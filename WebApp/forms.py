from django import forms
from .models import GeneralInformation, Tutorial


class GeneralInformationForm(forms.ModelForm):
    class Meta:
        model = GeneralInformation
        fields = '__all__'


class TutorialForm(forms.ModelForm):
    class Meta:
        model = Tutorial
        fields = '__all__'
