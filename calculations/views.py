# implement logic for tax calculations
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django_ratelimit.decorators import ratelimit
from django.conf import settings      
import logging
import json


logger = logging.getLogger('tax_calculator')
@ratelimit(key='ip', rate='5/m', block=True)  # 5 requests per minute per IP
@csrf_exempt  # Only for development, remove in production with proper CSRF handling
@require_POST

def calculate_tax(request):
    try:
        data = json.loads(request.body)
        income = float(data.get('income', 0))
        deductions = float(data.get('deductions', 0))
        year = data.get('year', '2025')  # Default to current year
        logger.info(f"Tax calculation request from IP: {request.META.get('REMOTE_ADDR')}")
        data = json.loads(request.body)
        
        # Input validation with logging
        income = float(data.get('income', 0))
        if income <= 0:
            logger.warning(f"Invalid income value received: {income}")
            return JsonResponse({'success': False, 'error': 'Income must be positive'}, status=400)    
        
        # Calculate taxable income
        taxable_income = income - deductions
        
        # Kenya tax calculation logic
        tax = 0
        if taxable_income <= 288000:
            tax = taxable_income * 0.1
        elif taxable_income <= 388000:
            tax = 28800 + (taxable_income - 288000) * 0.25
        else:
            tax = 28800 + 25000 + (taxable_income - 388000) * 0.3
        
        # Calculate NHIF and NSSF
        nhif = min(1700, income * 0.015)
        nssf = min(1080, income * 0.06)
        
        total_deductions = tax + nhif + nssf
        net_salary = income - total_deductions
        
        response_data = {
            'success': True,
            'results': {
                'gross_income': income,
                'taxable_income': taxable_income,
                'income_tax': tax,
                'nhif': nhif,
                'nssf': nssf,
                'net_salary': net_salary
            }
        }
        
        logger.info(f"Successful tax calculation for income: {income}, year: {year}")
        return JsonResponse(response_data)
    
    except Exception as e:
        logger.error(f"Error in tax calculation: {str(e)}", exc_info=True)
        return JsonResponse({'success': False, 'error': str(e)}, status=400)