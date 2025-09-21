from django.contrib import admin
from .models import SalesReport, ProductPerformance, UserActivity

@admin.register(SalesReport)
class SalesReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'total_revenue', 'total_orders', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ProductPerformance)
class ProductPerformanceAdmin(admin.ModelAdmin):
    list_display = ('product', 'report', 'units_sold', 'revenue', 'conversion_rate')
    search_fields = ('product__name', 'report__name')

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'created_at')
    list_filter = ('activity_type', 'created_at')
    search_fields = ('user__email', 'description')