from django import forms
from django.utils.safestring import mark_safe


class ImageWidget(forms.FileInput):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value:
            output.append(f'<img src="{value.url}" alt="Imagen actual" style="max-width: 200px; max-height: 200px;">')
        output.append(super().render(name, value, attrs))
        return mark_safe(u''.join(output))
