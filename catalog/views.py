from django.shortcuts import render, get_object_or_404

from .models import Product


# Create your views here.

def home(request):
    products = Product.objects.all()  # ORM-запрос на получение списка продуктов
    context = {
        'products': products
    }
    return render(request, 'home_page/home.html', context)


def contacts(request):
    return render(request, 'home_page/contacts.html')


def product_detail(request, pk):
    """Контроллер для отображения страницы с подробной информацией о товаре"""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'home_page/product_detail.html', {'product': product})
