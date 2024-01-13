from django import template
from django.db.models import Sum

register = template.Library()

@register.filter
def sum(queryset, field_name):
    return queryset.aggregate(Sum(field_name))['{}__sum'.format(field_name)]
