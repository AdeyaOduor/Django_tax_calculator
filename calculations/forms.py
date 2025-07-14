from django import forms

class IncomeForm(forms.Form):
    total_income = forms.FloatField(label='Total Income', min_value=0)

class TaxCalculationForm(forms.Form):
    income = forms.FloatField(min_value=0)
    deductions = forms.FloatField(min_value=0, required=False)
    year = forms.ChoiceField(choices=[('2023', '2023'), ('2024', '2024')])