django-admin startproject tax_calculator
cd tax_calculator
django-admin startapp calculations

pip install django-ratelimit

# tax_calculator/settings.py
INSTALLED_APPS = [
    ...
    'calculations',


# Create the following file inside calculations folder: forms.py, views.py,urls.py

# calculations/urls.py, set up URL, for calculation views


''' 
tax_calculator/
├── static/
│   └── css/
│       └── styles.css
├── templates/
│   ├── base.html
│   └── tax_calculator.html
├── __init__.py
├── admin.py
├── apps.py
├── forms.py
├── models.py
├── tests.py
├── urls.py
└── views.py

Run Migrations
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


To complete the setup:

    Run python manage.py collectstatic in production

    Configure your web server (Nginx/Apache) to serve static files

    Set up proper CSRF protection in production (remove @csrf_exempt)
'''
