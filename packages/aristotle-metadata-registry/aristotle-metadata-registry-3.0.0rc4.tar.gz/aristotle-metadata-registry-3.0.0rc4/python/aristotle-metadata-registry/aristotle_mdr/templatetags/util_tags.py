from django import template
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.html import format_html
from django.utils.safestring import mark_safe, SafeString
from django.conf import settings

import bleach

register = template.Library()


@register.filter
def order_by(qs, order):
    return qs.order_by(*(order.split(",")))


@register.filter
def startswith(string, substr):
    return string.startswith(substr)


@register.filter
def visible_count(model, user):
    return model.objects.all().visible(user).count()


@register.filter
def izip(a, b):
    return zip(a, b)


@register.filter
def register_queryset(qs):
    from aristotle_mdr.utils.cached_querysets import register_queryset
    return register_queryset(qs)


@register.filter
def distinct(iterable, attr_name):

    if not iterable:
        return []

    seen = []
    filtered = []
    for item in iterable:
        attr = getattr(item, attr_name)
        if attr not in seen:
            filtered.append(item)
            seen.append(attr)

    return filtered


@register.filter
def json_script(value, element_id):
    """
    Taken from Django 2.1

    Escape all the HTML/XML special characters with their unicode escapes, so
    value is safe to be output anywhere except for inside a tag attribute. Wrap
    the escaped JSON in a script tag.
    """

    _json_script_escapes = {
        ord('>'): '\\u003E',
        ord('<'): '\\u003C',
        ord('&'): '\\u0026',
    }

    json_str = json.dumps(value, cls=DjangoJSONEncoder).translate(_json_script_escapes)
    return format_html(
        '<script id="{}" type="application/json">{}</script>',
        element_id, mark_safe(json_str)
    )


@register.filter(name='bleach')
def bleach_filter(html: str) -> SafeString:

    if html is None:
        return html

    clean_html = bleach.clean(
        html,
        tags=settings.BLEACH_ALLOWED_TAGS,
        attributes=settings.BLEACH_ALLOWED_ATTRIBUTES
    )
    return mark_safe(clean_html)
