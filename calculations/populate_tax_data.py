from django.core.management.base import BaseCommand
from tax_calculator.models import TaxBracket, NHIFRate, NSSFRate

class Command(BaseCommand):
    help = 'Populates initial tax data'
    
    def handle(self, *args, **options):
        # 2023 Tax Brackets (Kenya example)
        TaxBracket.objects.bulk_create([
            TaxBracket(year=2023, lower_bound=0, upper_bound=288000, rate=0.1, fixed_amount=0),
            TaxBracket(year=2023, lower_bound=288001, upper_bound=388000, rate=0.25, fixed_amount=28800),
            TaxBracket(year=2023, lower_bound=388001, upper_bound=None, rate=0.3, fixed_amount=53800),
        ])
        
        # NHIF Rates
        NHIFRate.objects.bulk_create([
            NHIFRate(year=2023, lower_bound=0, upper_bound=5999, amount=150),
            NHIFRate(year=2023, lower_bound=6000, upper_bound=7999, amount=300),
            # Add more brackets as needed
            NHIFRate(year=2023, lower_bound=100000, upper_bound=None, amount=1700),
        ])
        
        # NSSF Rates (Kenya tiered system)
        NSSFRate.objects.bulk_create([
            NSSFRate(year=2023, tier='I', lower_bound=0, upper_bound=6000, employee_rate=0.06, employer_rate=0.06),
            NSSFRate(year=2023, tier='II', lower_bound=6001, upper_bound=18000, employee_rate=0.06, employer_rate=0.06),
        ])
        
        self.stdout.write(self.style.SUCCESS('Successfully populated tax data'))