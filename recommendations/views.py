from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count
from .models import Recommendation, UserBehavior
from .serializers import RecommendationSerializer
from products.models import Product
from products.serializers import ProductSerializer

class RecommendationListView(generics.ListAPIView):
    serializer_class = RecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Recommendation.objects.filter(user=self.request.user)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_recommendations(request):
    # Simple recommendation algorithm based on user behavior
    user = request.user
    
    # Get user's behavior history
    user_behaviors = UserBehavior.objects.filter(user=user)
    
    # If no behavior history, return popular products
    if not user_behaviors.exists():
        # Get products with highest average ratings
        popular_products = Product.objects.filter(
            reviews__is_approved=True
        ).annotate(
            review_count=Count('reviews')
        ).filter(
            review_count__gte=3
        ).order_by('-rating')[:10]
        
        serializer = ProductSerializer(popular_products, many=True)
        return Response(serializer.data)
    
    # Get products from same categories as user's behavior
    user_categories = Product.objects.filter(
        behaviors__user=user
    ).values_list('category', flat=True).distinct()
    
    # Recommend products from those categories with high ratings
    recommended_products = Product.objects.filter(
        category__in=user_categories,
        reviews__is_approved=True
    ).exclude(
        behaviors__user=user,
        behaviors__behavior_type='purchase'
    ).annotate(
        review_count=Count('reviews')
    ).filter(
        review_count__gte=1
    ).order_by('-rating', '-review_count')[:10]
    
    serializer = ProductSerializer(recommended_products, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def track_user_behavior(request):
    product_id = request.data.get('product')
    behavior_type = request.data.get('behavior_type', 'view')
    
    if not product_id:
        return Response({'error': 'Product ID is required'}, status=400)
    
    product = get_object_or_404(Product, id=product_id)
    
    # Create or update user behavior
    UserBehavior.objects.get_or_create(
        user=request.user,
        product=product,
        behavior_type=behavior_type
    )
    
    return Response({'message': 'Behavior tracked successfully'})

# Simple collaborative filtering recommendation
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_collaborative_recommendations(request):
    user = request.user
    
    # Find users with similar behavior
    similar_users = UserBehavior.objects.filter(
        product__behaviors__user=user
    ).exclude(
        user=user
    ).values('user').annotate(
        common_products=Count('product')
    ).filter(
        common_products__gte=2
    ).order_by('-common_products')[:5]
    
    if not similar_users:
        # If no similar users, return popular products
        return get_recommendations(request)
    
    # Get products liked by similar users that current user hasn't interacted with
    similar_user_ids = [u['user'] for u in similar_users]
    
    recommended_products = Product.objects.filter(
        behaviors__user__in=similar_user_ids,
        behaviors__behavior_type__in=['purchase', 'wishlist']
    ).exclude(
        behaviors__user=user
    ).annotate(
        recommendation_score=Count('behaviors')
    ).order_by('-recommendation_score')[:10]
    
    serializer = ProductSerializer(recommended_products, many=True)
    return Response(serializer.data)