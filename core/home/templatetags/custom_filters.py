from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='div')
def div(value, arg):
    """Divide the value by the argument"""
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return 0

@register.filter(name='mul')
def mul(value, arg):
    """Multiply the value by the argument"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter(name='min')
def min_filter(value, arg):
    """Return the minimum of value and arg"""
    try:
        return min(float(value), float(arg))
    except (ValueError, TypeError):
        return 0 