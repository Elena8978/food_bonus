from django.contrib import admin
from .models import Client, Dish, Order

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'bonus_balance', 'is_staff')
    list_filter = ('is_staff',)
    search_fields = ('username', 'email')


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image')
    search_fields = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'dish', 'client', 'created_at')
    list_filter = ('client', 'created_at')
    search_fields = ('dish__name', 'client__username')