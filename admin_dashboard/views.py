from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import SalesReport, ProductPerformance, UserActivity
from .serializers import SalesReportSerializer, ProductPerformanceSerializer, UserActivitySerializer
from orders.models import Order, OrderItem
from products.models import Product
from accounts.models import User

class SalesReportListView(generics.ListAPIView):
    serializer_class = SalesReportSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        return SalesReport.objects.all().order_by('-created_at')

class SalesReportDetailView(generics.RetrieveAPIView):
    serializer_class = SalesReportSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        return SalesReport.objects.all()

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def get_dashboard_stats(request):
    # Get key metrics for the dashboard
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_users = User.objects.count()
    
    # Revenue in the last 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_revenue = Order.objects.filter(
        created_at__gte=thirty_days_ago,
        status='completed'
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Recent orders
    recent_orders = Order.objects.filter(
        created_at__gte=thirty_days_ago
    ).count()
    
    stats = {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_users': total_users,
        'recent_revenue': float(recent_revenue),
        'recent_orders': recent_orders
    }
    
    return Response(stats)

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def get_top_products(request):
    # Get top selling products
    top_products = Product.objects.annotate(
        total_sold=Sum('order_items__quantity')
    ).filter(
        total_sold__gt=0
    ).order_by('-total_sold')[:10]
    
    serializer = ProductSerializer(top_products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def get_recent_orders(request):
    # Get recent orders
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:10]
    
    serializer = OrderSerializer(recent_orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def get_user_activity(request):
    # Get recent user activity
    recent_activity = UserActivity.objects.select_related('user').order_by('-created_at')[:20]
    
    serializer = UserActivitySerializer(recent_activity, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def generate_sales_report(request):
    # Generate a sales report
    name = request.data.get('name', 'Sales Report')
    days = int(request.data.get('days', 30))
    
    end_date = timezone.now()
    start_date = end_date - timedelta(days=days)
    
    # Calculate report data
    orders = Order.objects.filter(
        created_at__gte=start_date,
        created_at__lte=end_date,
        status='completed'
    )
    
    total_revenue = orders.aggregate(total=Sum('total_amount'))['total'] or 0
    total_orders = orders.count()
    
    # Calculate total products sold
    total_products_sold = OrderItem.objects.filter(
        order__in=orders
    ).aggregate(total=Sum('quantity'))['total'] or 0
    
    # Create sales report
    report = SalesReport.objects.create(
        name=name,
        start_date=start_date,
        end_date=end_date,
        total_revenue=total_revenue,
        total_orders=total_orders,
        total_products_sold=total_products_sold
    )
    
    serializer = SalesReportSerializer(report)
    return Response(serializer.data, status=status.HTTP_201_CREATED)