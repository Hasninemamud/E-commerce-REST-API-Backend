from django.urls import path
from . import views

urlpatterns = [
    path('', views.WishlistDetailView.as_view(), name='wishlist-detail'),
    path('add/', views.add_to_wishlist, name='wishlist-add'),
    path('remove/<int:item_id>/', views.remove_from_wishlist, name='wishlist-remove'),
]