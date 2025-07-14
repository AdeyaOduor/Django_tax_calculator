from django.db import models
from django.core.validators import MinValueValidator

class TaxBracket(models.Model):
    year = models.PositiveIntegerField()
    lower_bound = models.DecimalField(max_digits=12, decimal_places=2)
    upper_bound = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    rate = models.DecimalField(max_digits=5, decimal_places=4)
    fixed_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    class Meta:
        unique_together = ('year', 'lower_bound')
        ordering = ['year', 'lower_bound']
    
    def __str__(self):
        return f"{self.year} | {self.lower_bound} - {self.upper_bound or '∞'} @ {self.rate*100}%"

class NHIFRate(models.Model):
    year = models.PositiveIntegerField()
    lower_bound = models.DecimalField(max_digits=12, decimal_places=2)
    upper_bound = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    class Meta:
        unique_together = ('year', 'lower_bound')

class NSSFRate(models.Model):
    year = models.PositiveIntegerField()
    tier = models.CharField(max_length=1)
    lower_bound = models.DecimalField(max_digits=12, decimal_places=2)
    upper_bound = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    employee_rate = models.DecimalField(max_digits=5, decimal_places=4)
    employer_rate = models.DecimalField(max_digits=5, decimal_places=4)
    
    class Meta:
        unique_together = ('year', 'tier')

class TaxCalculation(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    income = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    year = models.PositiveIntegerField()
    taxable_income = models.DecimalField(max_digits=12, decimal_places=2)
    income_tax = models.DecimalField(max_digits=12, decimal_places=2)
    nhif = models.DecimalField(max_digits=12, decimal_places=2)
    nssf = models.DecimalField(max_digits=12, decimal_places=2)
    net_salary = models.DecimalField(max_digits=12, decimal_places=2)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Tax Calc #{self.id} - {self.income} ({self.year})"
# Create your models here.
