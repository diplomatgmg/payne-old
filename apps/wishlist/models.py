from django.db import models
from django.utils.translation import gettext_lazy as _

from ..shop.models import Product
from ..users.models import CustomUser


# Create your models here.
class WishlistItemQuerySet(models.QuerySet):
    def list_products(self):
        return (product.product for product in self)


class WishlistItem(models.Model):
    user = models.ForeignKey(CustomUser, null=False, blank=False, on_delete=models.CASCADE,
                             verbose_name=_('пользователь'))
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE, verbose_name=_('товар'))

    objects = WishlistItemQuerySet.as_manager()

    class Meta:
        verbose_name = 'избранное'
        verbose_name_plural = 'избранные'

    def __str__(self):
        return self.product.name
