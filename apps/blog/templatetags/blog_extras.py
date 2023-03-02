from django import template

register = template.Library()


@register.filter('shortify_post')
def shortify_post(post_desc: str):
    return post_desc.split('.', 1)[0] + '.'
