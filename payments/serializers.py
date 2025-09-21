from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('user', 'transaction_id', 'payment_intent_id', 'client_secret', 'created_at', 'updated_at')

class PaymentIntentSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    payment_method = serializers.CharField(max_length=20)