from django import template

from acmin.utils import attr2 as p

register = template.Library()


@register.filter
def attr2(value, attr_name):
    return p(value, attr_name, default="")
