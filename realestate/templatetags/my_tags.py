from django import template
from django.db.models import Sum

register = template.Library()

@register.filter
def modulo(num, val):
    return num % val

@register.filter
def divide(num, val):
    return num / val

@register.filter
def isequal(num, val):
    if num == val:
        return 1
    else:
        return 0

@register.filter
def in_property(things, category):
    return things.filter(property_name__icontains = category)

@register.filter
def extract_date(datetime):
    return datetime.purchase_date.date()

@register.filter
def is_empty_query(queries):
    if queries.exists():
        return 0
    else:
        return 1

@register.filter
def in_purchase(purchases, query):
    return purchases.filter(agent = query)

@register.filter
def is_available(properties, el):
    if el == 1:
        return properties.filter(is_available = True)
    else:
        return properties.filter(is_available = False)

