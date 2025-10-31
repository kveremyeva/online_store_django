from django.shortcuts import get_object_or_404
from .models import Category, Product


def get_products_by_category(category_id):
    """Сервисная функция для получения всех продуктов в указанной категории"""
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category, is_published=True)
    return products