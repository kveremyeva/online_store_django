from django import forms
from django.core.exceptions import ValidationError

from .models import Category, Product

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class ProductForm(forms.ModelForm):
    FORBIDDEN_WORDS = [
        'казино', 'криптовалюта', 'крипта', 'биржа',
        'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
    ]
    class Meta:
        model = Product
        fields = ['name', 'description',  'image', 'category', 'price', 'is_published']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите название'
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите описание'
        })
        self.fields['image'].widget.attrs.update({
            'class': 'form-control file-input'
        })
        self.fields['category'].widget.attrs.update({
            'class': 'form-select'
        })
        self.fields['price'].widget.attrs.update({
            'class': 'form-control price-input',
            'placeholder': '0.00'
        })
        self.fields['is_published'].widget.attrs.update({
            'class': 'form-check-input'
        })

    def clean_name(self):
        """Валидация названия продукта"""
        name = self.cleaned_data['name'].lower()

        for word in self.FORBIDDEN_WORDS:
            if word in name:
                raise forms.ValidationError(
                    f'Название содержит запрещенное слово: "{word}"'
                )

        return self.cleaned_data['name']

    def clean_description(self):
        """Валидация описания продукта"""
        description = self.cleaned_data['description'].lower()

        for word in self.FORBIDDEN_WORDS:
            if word in description:
                raise forms.ValidationError(
                    f'Описание содержит запрещенное слово: "{word}"'
                )

        return self.cleaned_data['description']

    def clean_price(self):
        """Кастомная валидация для поля price"""
        price = self.cleaned_data.get('price')

        if price is not None and price < 0:
            raise ValidationError('Цена не может быть отрицательной. Пожалуйста, введите положительное значение.')

        return price