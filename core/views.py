from django.shortcuts import render, redirect
from django.db import transaction
from .models import Product, Order, OrderItem, Payment, Employee, Recipe
import json


def pos_view(request):
    products = Product.objects.filter(is_available=True)
    return render(request, 'pos.html', {'products': products})


def create_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cart = data.get('cart', [])

        if not cart:
            return redirect('pos_view')

        try:
            with transaction.atomic():
                employee = Employee.objects.first()
                if not employee:
                    return redirect('pos_view')

                new_order = Order.objects.create(employee=employee, status='Оплачен')
                total_price = 0

                for item in cart:
                    product = Product.objects.get(id=item['id'])
                    qty = item['qty']
                    item_total = product.price * qty
                    total_price += item_total

                    OrderItem.objects.create(
                        order=new_order,
                        product=product,
                        quantity=qty,
                        price_at_moment=product.price
                    )

                    recipes = Recipe.objects.filter(product=product)
                    for recipe in recipes:
                        ingredient = recipe.ingredient
                        ingredient.stock_qty -= (recipe.amount * qty)
                        ingredient.save()

                new_order.total_price = total_price
                new_order.save()

                Payment.objects.create(
                    order=new_order,
                    payment_method='Карта',
                    amount=total_price
                )

            return redirect('pos_view')

        except Exception as e:
            print(f"Ошибка: {e}")
            return redirect('pos_view')