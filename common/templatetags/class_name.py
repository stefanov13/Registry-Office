from django import template

register = template.Library()

@register.filter(name='cls_name')
def class_name(obj):
    return obj.__class__.__name__
