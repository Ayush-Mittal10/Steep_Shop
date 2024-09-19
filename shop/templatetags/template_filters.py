from django import template

from shop.models import ProductVariant

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    if dictionary is None:
        return None
    return dictionary.get(str(key))

@register.filter(name='get_price')
def get_price(variants, size):
    print(variants)
    try:
        return variants.get(size=size).price
    except ProductVariant.DoesNotExist:
        return None