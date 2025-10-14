from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProductForm
from .models import Product

class ProductListView(ListView):
    """CBV для главной страницы со списком товаров"""
    model = Product
    template_name = 'home_page/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        """ORM-запрос на получение списка продуктов"""
        return Product.objects.all()


class ContactsView(TemplateView):
    """CBV для страницы контактов"""
    template_name = 'home_page/contacts.html'


class ProductDetailView(DetailView):
    """CBV для страницы с подробной информацией о товаре"""
    model = Product
    template_name = 'home_page/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        """Получение объекта товара с обработкой 404"""
        return get_object_or_404(Product, pk=self.kwargs['pk'])

class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание нового продукта"""
    model = Product
    form_class = ProductForm
    template_name = 'home_page/product_form.html'
    success_url = reverse_lazy('home')

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование существующего продукта"""
    model = Product
    form_class = ProductForm
    template_name = 'home_page/product_form.html'
    success_url = reverse_lazy('home')

class ProductDeleteView(DeleteView):
    """Удаление продукта"""
    model = Product
    template_name = 'home_page/product_confirm_delete.html'
    success_url = reverse_lazy('home')