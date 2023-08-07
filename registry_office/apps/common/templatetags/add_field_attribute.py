from django import template

register = template.Library()

@register.filter(name='disabled_field')
def disabled_field(form, field_names):
    field_names = field_names.split(',')
    for field_name in field_names:
        field = form[field_name]
        field.field.widget.attrs['disabled'] = True
    return form
