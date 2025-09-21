from django.urls import path
from .views import CreatePaymentIntentView, ConfirmPaymentView, PaymentListView, PaymentDetailView, stripe_webhook

urlpatterns = [
    path('', PaymentListView.as_view(), name='payment-list'),
    path('<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),
    path('create-intent/', CreatePaymentIntentView.as_view(), name='create-payment-intent'),
    path('webhook/', stripe_webhook, name='stripe-webhook'),
    path('<int:pk>/confirm/', ConfirmPaymentView.as_view(), name='confirm-payment'),
]
