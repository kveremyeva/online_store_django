from django.urls import path
from .apps import CatalogConfig
from .views import ContactsView, ProductListView, ProductDetailView

app_name = CatalogConfig.name

urlpatterns = [
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('home/', ProductListView.as_view(), name='home'),
    path('product_detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail')
]
