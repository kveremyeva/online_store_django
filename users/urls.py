from django.urls import path
from .views import RegisterView, CustomLoginView, CustomLogoutView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', CustomLogoutView.as_view(next_page='users:logout'), name='logout'),
]