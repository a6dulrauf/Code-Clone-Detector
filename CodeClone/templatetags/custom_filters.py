from django import template


register = template.Library()

@register.filter(name='Index')
def get_at_index(list, index):
    return list[index]