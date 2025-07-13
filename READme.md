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
