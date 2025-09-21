from django.contrib import admin
from .models import Recommendation, UserBehavior

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'score', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'product__name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(UserBehavior)
class UserBehaviorAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'behavior_type', 'created_at')
    list_filter = ('behavior_type', 'created_at')
    search_fields = ('user__email', 'product__name')