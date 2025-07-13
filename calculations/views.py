# implement logic for tax calculations
from django.shortcuts import render
from .forms import IncomeForm

def calculate_tax(request):
    tax = 0
    total_income = None

    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            total_income = form.cleaned_data['total_income']

            if total_income <= 144000:
                tax = 0
            else:
                taxable_income = total_income - 144000
                tax = taxable_income * 0.14 - 13994

                if tax < 0:
                    tax = 0
    else:
        form = IncomeForm()

    return render(request, 'calculations/tax_calculator.html', {
        'form': form,
        'total_income': total_income,
        'tax': tax,
    })
