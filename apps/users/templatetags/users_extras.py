from django import template

register = template.Library()


@register.filter('get_total_queryset')
def get_total_queryset(query):
    return sum(product.get_total_price() for product in query)
