from django.urls import path
from . import views

urlpatterns = [
    path('', views.RecommendationListView.as_view(), name='recommendation-list'),
    path('for-you/', views.get_recommendations, name='recommendations-for-you'),
    path('collaborative/', views.get_collaborative_recommendations, name='collaborative-recommendations'),
    path('track/', views.track_user_behavior, name='track-behavior'),
]