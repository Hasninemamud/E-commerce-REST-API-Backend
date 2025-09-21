from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()

class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-score']

    def __str__(self):
        return f"Recommendation for {self.user.email}: {self.product.name}"

class UserBehavior(models.Model):
    BEHAVIOR_TYPES = [
        ('view', 'View'),
        ('click', 'Click'),
        ('purchase', 'Purchase'),
        ('wishlist', 'Add to Wishlist'),
        ('cart', 'Add to Cart'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='behaviors')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    behavior_type = models.CharField(max_length=20, choices=BEHAVIOR_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} {self.behavior_type} {self.product.name}"