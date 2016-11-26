from django import template

register = template.Library()


@register.filter
def pageordered2(value, arg1):
    print(value, arg1)
    return value + arg1