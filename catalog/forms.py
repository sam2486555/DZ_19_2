from django.forms import ModelForm, forms, BooleanField

from catalog.models import Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs['class'] = "form-check-input"

            else:
                fild.widget.attrs['class'] = "form-control"




class ProductForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        exclude = '__all__'

        def clean_title(self):
            cleaned_data = self.cleaned_data.get('title')

            if cleaned_data in (
                    'казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар'):
                raise forms.ValidationError('Ошибка, связанная с вводом запрещенных слов')

            return cleaned_data

        def clean_desk(self):
            cleaned_data = self.cleaned_data.get('desk')

            if cleaned_data in (
                    'казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар'):
                raise forms.ValidationError('Ошибка, связанная с вводом запрещенных слов')

            return cleaned_data


class VersionForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Version
        exclude = '__all__'
