from rest_framework import serializers
from .models import Review, ReviewImage
from products.serializers import ProductSerializer
from accounts.serializers import UserSerializer

class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ['id', 'image', 'created_at']

class ReviewSerializer(serializers.ModelSerializer):
    images = ReviewImageSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'product', 'user', 'rating', 'comment', 'is_verified_purchase', 
                  'is_approved', 'created_at', 'updated_at', 'images']
        read_only_fields = ['user', 'is_approved']

class ReviewCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Review
        fields = ['id', 'product', 'rating', 'comment', 'is_verified_purchase', 'images']
        
    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        review = Review.objects.create(**validated_data)
        
        for image_data in images_data:
            ReviewImage.objects.create(review=review, image=image_data)
            
        return review