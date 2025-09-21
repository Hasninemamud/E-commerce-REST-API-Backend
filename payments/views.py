import stripe
from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Payment
from .serializers import PaymentSerializer, PaymentIntentSerializer
from orders.models import Order
from rest_framework.views import APIView

# Set your secret key: remember to change this to your live secret key in production

stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

class PaymentDetailView(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

class CreatePaymentIntentView(generics.CreateAPIView):
    serializer_class = PaymentIntentSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        order_id = serializer.validated_data['order_id']
        payment_method = serializer.validated_data['payment_method']
        
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            # Create a PaymentIntent with the order amount
            intent = stripe.PaymentIntent.create(
                amount=int(order.total_amount * 100),  # Amount in cents
                currency='usd',
                metadata={'order_id': order_id},
            )
            
            # Create or update payment record
            payment, created = Payment.objects.get_or_create(
                order=order,
                user=request.user,
                defaults={
                    'amount': order.total_amount,
                    'currency': 'usd',
                    'payment_method': payment_method,
                    'payment_intent_id': intent.id,
                    'client_secret': intent.client_secret,
                }
            )
            
            if not created:
                payment.amount = order.total_amount
                payment.payment_method = payment_method
                payment.payment_intent_id = intent.id
                payment.client_secret = intent.client_secret
                payment.save()
            
            return Response({
                'client_secret': intent.client_secret,
                'payment_id': payment.id
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ConfirmPaymentView(generics.UpdateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        payment = self.get_object()
        payment.payment_status = 'completed'
        payment.save()
        
        # Update order status
        payment.order.status = 'processing'
        payment.order.save()
        
        serializer = self.get_serializer(payment)
        return Response(serializer.data)


from rest_framework.views import APIView

class CreateCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        YOUR_DOMAIN = getattr(settings, 'FRONTEND_URL', "http://127.0.0.1:8000")
        order_id = request.data.get("order_id")  # Use request.data for DRF
        
        if not order_id:
            return Response({"error": "order_id is required"}, status=400)

        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f"Order #{order.id}",
                        },
                        'unit_amount': int(order.total_amount * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=YOUR_DOMAIN + f'/success/?session_id={{CHECKOUT_SESSION_ID}}',
                cancel_url=YOUR_DOMAIN + '/cancel/',
                metadata={'order_id': str(order_id)},
            )
            
            # Create payment record
            Payment.objects.get_or_create(
                order=order,
                user=request.user,
                defaults={
                    'amount': order.total_amount,
                    'currency': 'usd',
                    'payment_method': 'stripe',
                    'transaction_id': checkout_session.id,
                }
            )

            return Response({'checkout_url': checkout_session.url})
            
        except Exception as e:
            return Response({'error': str(e)}, status=400)

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        # Invalid payload
        return HttpResponse('Invalid payload', status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse('Invalid signature', status=400)

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']
        order_id = intent['metadata'].get('order_id')
        
        if order_id:
            try:
                with transaction.atomic():  # Add transaction safety
                    order = Order.objects.get(id=order_id)
                    payment = Payment.objects.get(payment_intent_id=intent['id'])
                    
                    if payment.payment_status != 'completed':  # Prevent duplicate processing
                        payment.payment_status = 'completed'
                        payment.transaction_id = intent['id']
                        payment.save()
                        
                        order.status = 'processing'
                        order.save()
                        
            except (Order.DoesNotExist, Payment.DoesNotExist) as e:
                # Log the error instead of silently passing
                logger.error(f"Webhook processing error: {e}")
    
    elif event['type'] == 'payment_intent.payment_failed':
        # Handle failed payments
        intent = event['data']['object']
        try:
            payment = Payment.objects.get(payment_intent_id=intent['id'])
            payment.payment_status = 'failed'
            payment.save()
        except Payment.DoesNotExist:
            pass

    return HttpResponse(status=200)