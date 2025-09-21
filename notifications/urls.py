from django.urls import path
from . import views

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notification-list'),
    path('<int:pk>/', views.NotificationDetailView.as_view(), name='notification-detail'),
    path('<int:notification_id>/read/', views.mark_notification_as_read, name='notification-mark-read'),
    path('read-all/', views.mark_all_notifications_as_read, name='notification-mark-all-read'),
]