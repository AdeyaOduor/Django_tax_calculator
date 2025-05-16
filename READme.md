django-admin startproject tax_calculator
cd tax_calculator
django-admin startapp calculations

Add the new app to your settings.py:

python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser

python manage.py runserver