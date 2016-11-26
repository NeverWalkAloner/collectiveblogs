from django import template

register = template.Library()


@register.filter
def pageordered(value, arg1):
    print(value, arg1)
    return (value - 1) * arg1
