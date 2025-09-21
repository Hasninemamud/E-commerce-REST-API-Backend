from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer
from products.models import Product
from django.shortcuts import get_object_or_404

class ReviewListView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        if product_id:
            return Review.objects.filter(product_id=product_id, is_approved=True)
        return Review.objects.filter(is_approved=True)
    
    def perform_create(self, serializer):
        product_id = self.request.data.get('product')
        product = get_object_or_404(Product, id=product_id)
        
        # Check if user has purchased the product (simplified for now)
        # In a real implementation, you would check order history
        is_verified_purchase = False
        
        serializer.save(user=self.request.user, is_verified_purchase=is_verified_purchase)

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_update(self, serializer):
        # Only allow users to update their own reviews
        if self.get_object().user == self.request.user:
            serializer.save()
        else:
            raise permissions.PermissionDenied("You can only update your own reviews.")
    
    def perform_destroy(self, instance):
        # Only allow users to delete their own reviews
        if instance.user == self.request.user:
            instance.delete()
        else:
            raise permissions.PermissionDenied("You can only delete your own reviews.")

class ProductReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Review.objects.filter(product_id=product_id, is_approved=True).order_by('-created_at')