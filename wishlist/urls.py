from django.urls import path
from .views import WishlistView, WishlistDeleteView

urlpatterns = [
    path('', WishlistView.as_view(), name='wishlist_list_create'),
    path('<int:pk>/remove/', WishlistDeleteView.as_view(), name='wishlist_remove'),
]