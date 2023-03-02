from django.urls import path

from .views import (UserWishlistView, wishlist_add, wishlist_clear,
                    wishlist_remove)

urlpatterns = [
    path('', UserWishlistView.as_view(), name='wishlist'),
    path('add/<int:product_id>/', wishlist_add, name='wishlist-add'),
    path('remove/<int:product_id>/', wishlist_remove, name='wishlist-remove'),
    path('clear/', wishlist_clear, name='wishlist-clear'),
]
