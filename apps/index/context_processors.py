from ..cart.models import CartItem
from ..wishlist.models import WishlistItem


def get_user_cart(request):
    user_cart = None
    if request.user.is_authenticated:
        user_cart = CartItem.objects.filter(user=request.user)

    return {'user_cart': user_cart}


def get_user_wishlist(request):
    wishlist = None
    if request.user.is_authenticated:
        wishlist = WishlistItem.objects.filter(user=request.user)

    return {'wishlist': wishlist}
