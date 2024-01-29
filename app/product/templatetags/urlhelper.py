from django.template import Library

register = Library()

@register.simple_tag
def edit_query(request, **kwargs):
    qd = request.GET.copy()
    
    for key, value in kwargs.items():
        qd[key] = value
    if 'page' in qd:
        del qd['page']

    return "?" + qd.urlencode()

@register.simple_tag
def edit_query_pagination(request, **kwargs):
    qd = request.GET.copy()
    
    for key, value in kwargs.items():
        qd[key] = value
    return "?" + qd.urlencode()