from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from ..wishlist.models import WishlistItem
from mixins.views import TitleMixin


# Create your views here.
class UserWishlistView(TitleMixin, LoginRequiredMixin, TemplateView):
    template_name = 'users/../../templates/wishlist/wishlist.html'
    title = 'Избранное'


@login_required
def wishlist_add(request, product_id):
    wishitem_user, created = WishlistItem.objects.get_or_create(user=request.user, product_id=product_id)
    if not created:
        wishitem_user.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def wishlist_clear(request):
    user_cart_products = WishlistItem.objects.filter(user=request.user)
    user_cart_products.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def wishlist_remove(request, product_id):
    WishlistItem.objects.get(user=request.user, product_id=product_id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
