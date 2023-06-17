from django import template

register = template.Library()


@register.filter(name='verbose_name')
def get_field_verbose_name(instance, field_name):
    return instance._meta.get_field(field_name).verbose_name.title()


@register.filter(name='field_type')
def field_type(field):
    return field.field.widget.__class__.__name__
