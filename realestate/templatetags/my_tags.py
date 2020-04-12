from django import template

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
