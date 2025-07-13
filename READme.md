django-admin startproject tax_calculator
cd tax_calculator
django-admin startapp calculations

# tax_calculator/settings.py
INSTALLED_APPS = [
    ...
    'calculations',
    
python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser

python manage.py runserver


# calculations/forms.py, create forms to capture user input
from django import forms

class IncomeForm(forms.Form):
    total_income = forms.FloatField(label='Total Income', min_value=0)

# calculations/views.py, implement logic for tax calculations
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

# calculations/urls.py, set up URL, for calculation views
from django.urls import path
from .views import calculate_tax

urlpatterns = [
    path('', calculate_tax, name='calculate_tax'),
]

# tax_calculator/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('calculations.urls')),
]

# Create template
<!-- calculations/templates/calculations/tax_calculator.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tax Calculator</title>
</head>
<body>
    <h1>Tax Calculator</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Calculate Tax</button>
    </form>

    {% if total_income is not None %}
        <h2>Tax Details:</h2>
        <p>Total Income: ${{ total_income }}</p>
        <p>Tax Amount: ${{ tax|floatformat:2 }}</p>
    {% endif %}
</body>
</html>

''' 
Run Migrations

Run the following commands to prepare your database (even though we are not using any models here):
bash

python manage.py makemigrations
python manage.py migrate

8. Create Superuser (Optional)

If you want to access the admin panel:
bash

python manage.py createsuperuser

9. Run the Server

Start the Django development server:
bash

python manage.py runserver
'''
