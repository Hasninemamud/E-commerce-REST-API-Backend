from rest_framework import serializers
from .models import SalesReport, ProductPerformance, UserActivity
from products.serializers import ProductSerializer
from orders.serializers import OrderSerializer
from accounts.serializers import UserSerializer

class ProductPerformanceSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = ProductPerformance
        fields = ['id', 'product', 'units_sold', 'revenue', 'views', 'conversion_rate']

class SalesReportSerializer(serializers.ModelSerializer):
    product_performances = ProductPerformanceSerializer(many=True, read_only=True)
    
    class Meta:
        model = SalesReport
        fields = ['id', 'name', 'start_date', 'end_date', 'total_revenue', 
                  'total_orders', 'total_products_sold', 'created_at', 'updated_at', 
                  'product_performances']

class UserActivitySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserActivity
        fields = ['id', 'user', 'activity_type', 'description', 'ip_address', 
                  'user_agent', 'created_at']