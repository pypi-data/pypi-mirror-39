from django import template

from acmin.utils import attr as u

register = template.Library()


@register.filter
def attr(value, attr_name):
    return u(value, attr_name, default="")
