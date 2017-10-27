import json

from django import template
from django.utils.safestring import mark_safe

from util import core_util

register = template.Library()


@register.filter(name='get_date_string')
def get_date_string(value):
    if value:
        return core_util.format_date(core_util.from_seconds(value))
    else:
        return 'Nan'


@register.filter(name='get_full_date_string')
def get_full_date_string(value):
    if value:
        return core_util.format_date(core_util.from_seconds(value))
    else:
        return 'Nan'


@register.filter(name='get_full_time_string')
def get_full_time_string(value):
    if value:
        return core_util.format_date_time(core_util.from_seconds(value))
    else:
        return 'Nan'


@register.filter(name='format_allocation_time')
def format_allocation_time(value):
    if value:
        value = int(float(value))
        hours = int(float(value / 60))
        minutes = int(float(value % 60))
        return "%s:%s" % (str(hours), str(minutes))
    else:
        return 'Nan'


@register.filter(name='at')
def at(l, i):
    try:
        return l[i]
    except:
        return None


@register.filter(name='is_in')
def is_in(var, obj):
    return var in obj


@register.filter(name='jsonify')
def jsonify(object):
    if object:
        return mark_safe(json.dumps(object))
    else:
        return mark_safe(json.dumps({}))


@register.filter(name='this_or_zero')
def this_or_zero(object):
    if object:
        return object
    else:
        return 0


@register.filter(name='to_str')
def to_str(object):
    return str(object)


@register.filter(name='index')
def index(List, i):
    return List[int(i)]
