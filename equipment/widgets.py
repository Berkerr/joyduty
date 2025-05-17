from django import forms
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe
from .models import EquipmentCategory

class MPTTModelChoiceWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        if attrs is None:
            attrs = {}
        final_attrs = self.build_attrs(attrs, {'class': 'mptt-widget'})
        output = '<ul{}>'.format(attrs)
        for category in EquipmentCategory.objects.all():
            output += '<li data-value="{}">{}</li>'.format(category.pk, category.name)
        output += '</ul>'
        return mark_safe(output)
