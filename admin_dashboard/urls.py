from django.urls import path
from . import views

urlpatterns = [
    path('reports/', views.SalesReportListView.as_view(), name='sales-report-list'),
    path('reports/<int:pk>/', views.SalesReportDetailView.as_view(), name='sales-report-detail'),
    path('stats/', views.get_dashboard_stats, name='dashboard-stats'),
    path('top-products/', views.get_top_products, name='top-products'),
    path('recent-orders/', views.get_recent_orders, name='recent-orders'),
    path('user-activity/', views.get_user_activity, name='user-activity'),
    path('generate-report/', views.generate_sales_report, name='generate-sales-report'),
]