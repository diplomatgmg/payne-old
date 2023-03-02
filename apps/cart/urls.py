from django.urls import path

from .views import (UserCartView, cart_add, cart_clear, cart_quantity_change,
                    cart_remove)
from .views import CheckoutView, apply_promo

urlpatterns = [
    path('', UserCartView.as_view(), name='cart'),
    path('add/<int:product_id>/', cart_add, name='cart-add'),
    path('remove/<int:product_id>/', cart_remove, name='cart-product-remove'),
    path('clear/', cart_clear, name='cart-clear'),
    path('change_quantity/<int:product_id>/', cart_quantity_change, name='change-quantity'),

    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('checkout/promo/', apply_promo, name='apply-promo'),
]
