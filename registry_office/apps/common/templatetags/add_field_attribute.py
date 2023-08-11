from django import template

register = template.Library()

@register.filter(name='disabled_field')
def disabled_field(form, field_names):
    field_names = field_names.split(',')

    for field_name in field_names:
        field = form[field_name]
        field.field.widget.attrs['disabled'] = True

    return form

@register.filter(name='add_field_classes')
def add_field_classes(field, css_classes):
    classes = field.field.widget.attrs.get('class', '').split()
    classes.extend(css_classes.split())
    field.field.widget.attrs['class'] = ' '.join(classes)
    
    return field
