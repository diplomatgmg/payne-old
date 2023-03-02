from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..shop.models import Product
from ..users.models import CustomUser


class CartQuerySet(models.QuerySet):
    def total_price(self, promo_code=None):
        cart_price = sum(cart_item.product.price * cart_item.quantity for cart_item in self)
        if not promo_code:
            return cart_price
        else:
            promo_discount = PromoCode.objects.get(promo_code=promo_code).discount
            return cart_price - (cart_price // 100 * promo_discount)

    def list_products(self):
        return (product.product for product in self)


class CartItem(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, verbose_name=_('пользователь'))
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name=_('товар'))
    quantity = models.PositiveIntegerField(_('количество'), default=1)
    updated = models.DateTimeField(_('создана'), auto_now=True)
    timestamp = models.DateTimeField(_('последние изменение'), auto_now_add=True)

    objects = CartQuerySet.as_manager()

    class Meta:
        verbose_name = _('предмет из корзины')
        verbose_name_plural = _('предметы из корзины')

    def product_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.name


class PromoCode(models.Model):
    promo_code = models.CharField(_('промокод'), max_length=20, blank=False, null=False)
    discount = models.PositiveSmallIntegerField(_('скидка (%)'), default=15)

    class Meta:
        verbose_name = _('промокод')
        verbose_name_plural = _('промокоды')

    def __str__(self):
        return self.promo_code


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name=_('пользователь'))
    first_name = models.CharField(_('имя'), max_length=64)
    last_name = models.CharField(_('фамилия'), max_length=64)

    city = models.CharField(_('город'), max_length=64)
    street = models.CharField(_('улица'), max_length=64)
    house = models.CharField(_('дом'), max_length=32)
    building = models.CharField(_('корпус'), max_length=32)
    apartment = models.CharField(_('квартира'), max_length=32)

    phone = models.CharField(_('телефон'), max_length=32)
    email = models.CharField(_('почта'), max_length=64)
    description = models.TextField(_('описание'), max_length=2048, blank=True)

    created = models.DateTimeField(_('создано'), auto_now_add=True)
    updated = models.DateTimeField(_('обновлено'), auto_now=True)
    promo_code = models.CharField(_('использованный промокод'), max_length=64, blank=True, null=True)

    real_price = models.IntegerField(_('итог без скидки'))
    total_price = models.IntegerField(_('итог'))
    discount = models.PositiveSmallIntegerField(_('скидка (%)'), blank=True, null=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = _('заказ')
        verbose_name_plural = _('заказы')

    def __str__(self):
        return f'Заказ №{self.id}, {self.first_name} {self.last_name}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_('заказ'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('товар'))
    quantity = models.PositiveIntegerField(_('количество'))

    class Meta:
        verbose_name = _('товар')
        verbose_name_plural = _('товары')

    def __str__(self):
        return self.product.name
