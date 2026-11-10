from django.contrib import admin
from .models import (
    Role, Employee, Customer, Category, Product, Ingredient,
    Recipe, Order, OrderItem, Payment, Supplier, Supply, SupplyItem
)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_available', 'category')
    list_filter = ('category', 'is_available')

admin.site.register(Role)
admin.site.register(Employee)
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Supplier)
admin.site.register(Supply)
admin.site.register(SupplyItem)