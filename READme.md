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

<!-- write stord procedure in MySQL -->
DELIMITER //

-- Procedure to calculate income tax
CREATE PROCEDURE CalculateIncomeTax(
    IN p_income DECIMAL(12,2),
    IN p_deductions DECIMAL(12,2),
    IN p_year INT,
    OUT p_taxable_income DECIMAL(12,2),
    OUT p_income_tax DECIMAL(12,2)
)
BEGIN
    DECLARE v_remaining DECIMAL(12,2);
    DECLARE v_bracket_tax DECIMAL(12,2);
    
    SET p_taxable_income = p_income - IFNULL(p_deductions, 0);
    SET p_income_tax = 0;
    SET v_remaining = p_taxable_income;
    
    -- Get tax brackets ordered by lower bound
    DECLARE done INT DEFAULT FALSE;
    DECLARE cur CURSOR FOR 
        SELECT lower_bound, upper_bound, rate, fixed_amount 
        FROM tax_calculator_taxbracket 
        WHERE year = p_year 
        ORDER BY lower_bound;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN cur;
    
    read_loop: LOOP
        DECLARE v_lower DECIMAL(12,2);
        DECLARE v_upper DECIMAL(12,2);
        DECLARE v_rate DECIMAL(5,4);
        DECLARE v_fixed DECIMAL(12,2);
        
        FETCH cur INTO v_lower, v_upper, v_rate, v_fixed;
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        IF v_remaining <= 0 THEN
            LEAVE read_loop;
        END IF;
        
        IF v_upper IS NULL OR v_remaining <= v_upper - v_lower THEN
            SET v_bracket_tax = v_remaining * v_rate;
            SET v_remaining = 0;
        ELSE
            SET v_bracket_tax = (v_upper - v_lower) * v_rate;
            SET v_remaining = v_remaining - (v_upper - v_lower);
        END IF;
        
        SET p_income_tax = p_income_tax + v_bracket_tax + v_fixed;
    END LOOP;
    
    CLOSE cur;
END //

-- Procedure to calculate NHIF
CREATE PROCEDURE CalculateNHIF(
    IN p_income DECIMAL(12,2),
    IN p_year INT,
    OUT p_nhif DECIMAL(12,2)
)
BEGIN
    SELECT amount INTO p_nhif
    FROM tax_calculator_nhifrate
    WHERE year = p_year
    AND (p_income BETWEEN lower_bound AND IFNULL(upper_bound, 999999999))
    ORDER BY lower_bound DESC
    LIMIT 1;
    
    IF p_nhif IS NULL THEN
        SET p_nhif = 0;
    END IF;
END //

-- Procedure to calculate NSSF
CREATE PROCEDURE CalculateNSSF(
    IN p_income DECIMAL(12,2),
    IN p_year INT,
    OUT p_nssf DECIMAL(12,2)
)
BEGIN
    DECLARE v_tier1_max DECIMAL(12,2);
    DECLARE v_tier2_max DECIMAL(12,2);
    
    -- Get tier limits
    SELECT upper_bound INTO v_tier1_max
    FROM tax_calculator_nssfrate
    WHERE year = p_year AND tier = 'I';
    
    SELECT upper_bound INTO v_tier2_max
    FROM tax_calculator_nssfrate
    WHERE year = p_year AND tier = 'II';
    
    -- Calculate NSSF
    IF p_income <= v_tier1_max THEN
        SELECT employee_rate * LEAST(p_income, v_tier1_max) INTO p_nssf
        FROM tax_calculator_nssfrate
        WHERE year = p_year AND tier = 'I';
    ELSE
        SELECT 
            (SELECT employee_rate * v_tier1_max FROM tax_calculator_nssfrate WHERE year = p_year AND tier = 'I') +
            (SELECT employee_rate * LEAST(p_income - v_tier1_max, v_tier2_max - v_tier1_max) FROM tax_calculator_nssfrate WHERE year = p_year AND tier = 'II')
        INTO p_nssf;
    END IF;
    
    IF p_nssf IS NULL THEN
        SET p_nssf = 0;
    END IF;
END //

-- Main procedure to calculate all taxes
CREATE PROCEDURE CalculateAllTaxes(
    IN p_income DECIMAL(12,2),
    IN p_deductions DECIMAL(12,2),
    IN p_year INT,
    OUT p_taxable_income DECIMAL(12,2),
    OUT p_income_tax DECIMAL(12,2),
    OUT p_nhif DECIMAL(12,2),
    OUT p_nssf DECIMAL(12,2),
    OUT p_net_salary DECIMAL(12,2)
)
BEGIN
    -- Calculate taxable income
    SET p_taxable_income = p_income - IFNULL(p_deductions, 0);
    
    -- Call other procedures
    CALL CalculateIncomeTax(p_income, p_deductions, p_year, p_taxable_income, p_income_tax);
    CALL CalculateNHIF(p_income, p_year, p_nhif);
    CALL CalculateNSSF(p_income, p_year, p_nssf);
    
    -- Calculate net salary
    SET p_net_salary = p_income - p_income_tax - p_nhif - p_nssf;
END //

DELIMITER ;
<!-- ---------------------------------------------------------------------------------------------------------------- -->

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
