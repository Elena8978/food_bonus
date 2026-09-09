from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.dishes_view, name='dishes'),
    path('dishes/', views.dishes_view, name='dishes'),
    path('register/', views.register_view, name='register'),
    path('login/', LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('orders/create/', views.order_create, name='order_create'),
    path('orders/', views.orders_view, name='orders'),
]