from django.forms import ModelForm, forms, BooleanField

from catalog.models import Product, Version, Blog


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
        fields = '__all__'

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

class ProductModeratorForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        fields = ("published", "desk", "category")


class VersionForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Version
        fields = '__all__'

class BlogForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'


class BlogModeratorForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Blog
        fields = ("title", "content", "published",)