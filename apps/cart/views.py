from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic import TemplateView

from mixins.views import TitleMixin
from .forms import CheckoutForm
from .models import CartItem, PromoCode, Order, OrderItem


class UserCartView(TitleMixin, LoginRequiredMixin, TemplateView):
    template_name = 'cart/cart.html'
    title = 'Корзина'


@login_required
def cart_add(request, product_id):
    user_cart_product, created = CartItem.objects.get_or_create(user=request.user, product_id=product_id)
    if not created:
        user_cart_product.quantity += 1
        user_cart_product.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def cart_clear(request):
    CartItem.objects.filter(user=request.user).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def cart_remove(request, product_id):
    CartItem.objects.get(user=request.user, product_id=product_id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def cart_quantity_change(request, product_id):
    new_count = int(request.POST.get('quantity', 1))
    user_cart_product = CartItem.objects.get(user=request.user, product_id=product_id)
    total_product_quantity = user_cart_product.product.amount

    if new_count < total_product_quantity:
        user_cart_product.quantity = new_count
    else:
        user_cart_product.quantity = total_product_quantity

    user_cart_product.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class CheckoutView(FormView):
    template_name = 'checkout/checkout.html'
    form_class = CheckoutForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        promo_code = self.request.session.get('promo_code')
        form.cleaned_data['promo_code'] = promo_code
        cart_item_model = CartItem.objects.filter(user=self.request.user)
        total_price = cart_item_model.total_price(promo_code)
        real_price = cart_item_model.total_price()
        if promo_code:
            promo_model = PromoCode.objects.get(promo_code=promo_code)
            discount = promo_model.discount
        else:
            discount = 0

        order = Order.objects.create(user=self.request.user,
                                     total_price=total_price,
                                     discount=discount,
                                     real_price=real_price,
                                     **form.cleaned_data)

        for cart_item in CartItem.objects.filter(user=self.request.user):
            OrderItem.objects.create(order=order,
                                     product=cart_item.product,
                                     quantity=cart_item.quantity)

        cart_item_model.delete()
        self.request.session['promo_code'] = ''

        return HttpResponseRedirect(self.success_url)


def apply_promo(request):
    request_promo = request.GET.get('promo_code', '').lower()
    promo_model = PromoCode.objects.filter(promo_code=request_promo).last()
    if promo_model:
        request.session['promo_code'] = promo_model.promo_code
        request.session['promo_discount'] = promo_model.discount
        messages.success(request, 'Промокод успешно применен!')
    else:
        messages.error(request, 'Промокод не действителен!')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
