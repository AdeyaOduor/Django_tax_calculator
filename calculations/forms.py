# calculations/forms.py
from django import forms

class IncomeForm(forms.Form):
    total_income = forms.FloatField(label='Total Income', min_value=0)