django-admin startproject tax_calculator
cd tax_calculator
django-admin startapp calculations

pip install django-ratelimit
pip install mysqlclient

<!-- Create MySQL database: in mysql -->

CREATE DATABASE tax_calculator CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'tax_user'@'localhost' IDENTIFIED BY 'securepassword123';
GRANT ALL PRIVILEGES ON tax_calculator.* TO 'tax_user'@'localhost';
FLUSH PRIVILEGES;


<!-- import stored procedure on linux cli -->

mysql -u tax_user -p tax_calculator < mysql_procedures.sql

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

9. Run the Server: Start the Django development server in bash,

python manage.py populate_tax_data

python manage.py runserver


To complete the setup:

    Run python manage.py collectstatic in production

    Configure your web server (Nginx/Apache) to serve static files

    Set up proper CSRF protection in production (remove @csrf_exempt)
'''

# Git vertsion control steps in cli
git clone https://github.com/AdeyaOduor/tax_calculator.git
cd tax_calculator
code .

# modify and add files on vscode terminal,
git add .
git commit -m 'modified files'
git push origin main

# pull then push form vscode terminal,
git fetch origin
git rebase origin/main
git add .
git rebase --continue
git push origin main --force-with-lease


# 1. First, fetch the latest changes from remote
git fetch origin

# 2. Merge the remote changes into your local branch
git merge origin/your-branch-name

# 3. Resolve any merge conflicts if they occur
# (Open files with conflicts, edit them, then mark as resolved)
git add .
git commit -m "Merge remote changes"

# 4. Now push your changes
git push origin your-branch-name
