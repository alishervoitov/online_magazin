from django.urls import path
from .views import CartDetailView, AddToCartView, RemoveFromCartView

urlpatterns = [
    path('', CartDetailView.as_view(), name='cart_detail'),
    path('add/', AddToCartView.as_view(), name='cart_add'),
    path('item/<int:item_id>/remove/', RemoveFromCartView.as_view(), name='cart_item_remove'),

]


##https://makeupstore.uz/product/670216/
##https://makeupstore.uz/product/727524/
##https://makeupstore.uz/product/470742/