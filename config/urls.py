from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('catalog.urls')),
    path('catalog/', include('catalog.urls', namespace='home')),
    path('', include('catalog.urls', namespace='contacts'))
]
