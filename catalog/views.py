from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import ProductForm
from .models import Product, Category
from catalog.services import get_products_by_category


class ProductListView(ListView):
    """CBV для главной страницы со списком товаров"""
    model = Product
    template_name = 'home_page/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        """ORM-запрос на получение списка опубликованных продуктов"""
        user = self.request.user
        if user.is_staff or user.has_perm('catalog.can_unpublish_product'):
            cache_key = 'products_queryset_staff'
        else:
            cache_key = 'products_queryset_public'

        queryset = cache.get(cache_key)
        if not queryset:
            if user.is_staff or user.has_perm('catalog.can_unpublish_product'):
                queryset = Product.objects.all()
            else:
                queryset = Product.objects.filter(is_published=True)

            cache.set(cache_key, queryset, 60 * 15)

        return queryset

    def get_context_data(self, **kwargs):
        """Добавляем категории в контекст"""
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(product__is_published=True).distinct()
        return context


class ContactsView(TemplateView):
    """CBV для страницы контактов"""
    template_name = 'home_page/contacts.html'

@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(DetailView):
    """CBV для страницы с подробной информацией о товаре"""
    model = Product
    template_name = 'home_page/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        """Получение объекта товара с обработкой 404"""
        return get_object_or_404(Product, pk=self.kwargs['pk'])

class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Создание нового продукта"""
    model = Product
    form_class = ProductForm
    template_name = 'home_page/product_form.html'
    success_url = reverse_lazy('catalog:home')
    permission_required = 'catalog.add_product'

    def get_form_kwargs(self):
        """Передаем пользователя в форму"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Автоматически привязываем продукт к текущему пользователю"""
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Редактирование существующего продукта"""
    model = Product
    form_class = ProductForm
    template_name = 'home_page/product_form.html'
    success_url = reverse_lazy('catalog:home')
    permission_required = 'catalog.change_product'

    def get_form_kwargs(self):
        """Передаем пользователя в форму"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        product = get_object_or_404(Product, pk=pk)

        if not product.owner == request.user:
            return HttpResponseForbidden("У вас нет прав для редактирования этого продукта.")

        self.object = product

        return super().post(request, *args, **kwargs)


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Удаление продукта"""
    model = Product
    template_name = 'home_page/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')
    permission_required = 'catalog.delete_product'

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        product = get_object_or_404(Product, pk=pk)

        if not (product.owner == request.user
                or request.user.has_perm('catalog.delete_product')):
            return HttpResponseForbidden("У вас нет прав для удаления этого продукта.")

        self.object = product

        return super().post(request, *args, **kwargs)


class ProductUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """ Публикация продукта"""
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        if not (product.owner == request.user
                or request.user.has_perm('catalog.can_unpublish_product')):
            return HttpResponseForbidden("У вас нет прав для отмены публикации продукта.")

        product.is_published = False
        product.save()

        return redirect('catalog:product_detail', pk=product.pk)


class CategoryProductView(ListView):
    """CBV для отображения продуктов по категории"""
    model = Product
    template_name = 'home_page/category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        """Используем сервисную функцию для получения продуктов"""
        category_id = self.kwargs['pk']
        return get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        """Добавляем категорию в контекст"""
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs['pk']
        context['category'] = get_object_or_404(Category, id=category_id)
        return context