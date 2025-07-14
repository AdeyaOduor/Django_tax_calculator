# Register your models here.
from django.contrib import admin
from .models import TaxBracket, NHIFRate, NSSFRate, TaxCalculation

class TaxBracketAdmin(admin.ModelAdmin):
    list_display = ('year', 'lower_bound', 'upper_bound', 'rate', 'fixed_amount')
    list_filter = ('year',)
    search_fields = ('year',)

class NHIFRateAdmin(admin.ModelAdmin):
    list_display = ('year', 'lower_bound', 'upper_bound', 'amount')
    list_filter = ('year',)

class NSSFRateAdmin(admin.ModelAdmin):
    list_display = ('year', 'tier', 'lower_bound', 'upper_bound', 'employee_rate', 'employer_rate')
    list_filter = ('year', 'tier')

class TaxCalculationAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'income', 'year', 'net_salary')
    list_filter = ('year', 'timestamp')
    search_fields = ('user__username', 'ip_address')
    readonly_fields = ('timestamp',)

admin.site.register(TaxBracket, TaxBracketAdmin)
admin.site.register(NHIFRate, NHIFRateAdmin)
admin.site.register(NSSFRate, NSSFRateAdmin)
admin.site.register(TaxCalculation, TaxCalculationAdmin)
