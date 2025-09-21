from rest_framework import serializers
from .models import Recommendation, UserBehavior
from products.serializers import ProductSerializer
from accounts.serializers import UserSerializer

class RecommendationSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Recommendation
        fields = ['id', 'user', 'product', 'score', 'created_at', 'updated_at']

class UserBehaviorSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserBehavior
        fields = ['id', 'user', 'product', 'behavior_type', 'created_at']