from django import template

register = template.Library()

@register.filter(name='format_decimal')
def format_decimal(value, decimal_places=2):
    try:
        value = round(float(value), decimal_places)
        return '{:.{}f}'.format(value, decimal_places).replace(',', '.')
    except (ValueError, TypeError):
        return value