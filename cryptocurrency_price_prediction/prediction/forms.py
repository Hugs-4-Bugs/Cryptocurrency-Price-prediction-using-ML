from django import forms
from .model.data_collector import *


class PredictionForm(forms.Form):
    date = forms.DateField(label='Date', widget=forms.DateInput(attrs={'type': 'date'}))
    coin = forms.ChoiceField(choices=get_coin_list())

