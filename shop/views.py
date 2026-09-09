from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from decimal import Decimal
from .models import Dish, Order, Client
from .forms import RegistrationForm, OrderForm

def dishes_view(request):
    dishes = Dish.objects.all()
    return render(request, 'shop/dishes.html', {'dishes': dishes})

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрированы!')
            return redirect('/')
    else:
        form = RegistrationForm()
    return render(request, 'shop/register.html', {'form': form})

@login_required
def order_create(request):
    dish_id = request.GET.get('dish')
    initial_dish = None
    if dish_id:
        initial_dish = get_object_or_404(Dish, id=dish_id)

    if request.method == 'POST':
        form = OrderForm(request.POST, client=request.user)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.client = request.user
                order.save()

                user = request.user
                if form.cleaned_data.get('use_bonuses'):
                    user.bonus_balance = Decimal('0.00')
                    messages.info(request, 'Бонусы списаны')

                bonus = order.dish.price * Decimal('0.05')
                user.bonus_balance += bonus
                user.save()

                messages.success(request, f'Заказ оформлен! Начислено {bonus:.2f} бонусов')

            return redirect('/orders/')
    else:
        form = OrderForm(client=request.user)
        if initial_dish:
            form.fields['dish'].initial = initial_dish

    return render(request, 'shop/order_form.html', {'form': form})

@login_required
def orders_view(request):
    orders = request.user.orders.all()
    return render(request, 'shop/orders.html', {'orders': orders})