from django.urls import path
from .views import (ItemDetailView, contact, ItemsView, HomeView,
                    add_to_cart, remove_from_cart)
app_name = 'core'
urlpatterns = [
    path('produits/<slug>/', ItemDetailView, name='product'),
    path('contact/', contact, name='contact'),
    path('', HomeView, name='Home'),
    path('produits/', ItemsView.as_view(), name='products'),
    path('addToCart/<slug>/', add_to_cart, name='add_to_cart'),
    path('removeFromCart/<slug>/', remove_from_cart, name='remove_from_cart')
]
