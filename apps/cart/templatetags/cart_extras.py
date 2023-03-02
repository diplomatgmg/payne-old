from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


@register.simple_tag
def cart_promo(user_cart, promo_code):
    return intcomma(user_cart.total_price(promo_code))
