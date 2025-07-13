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


# Create the following file inside calculations folder: forms.py, views.py,urls.py

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
