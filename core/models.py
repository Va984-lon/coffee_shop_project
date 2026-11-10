from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=50, verbose_name="Наименование")
    def __str__(self): return self.name
    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"

class Employee(models.Model):
    role = models.ForeignKey(Role, on_delete=models.PROTECT, verbose_name="Роль")
    full_name = models.CharField(max_length=100, verbose_name="ФИО")
    login = models.CharField(max_length=50, unique=True, verbose_name="Логин")
    password = models.CharField(max_length=100, verbose_name="Пароль")
    def __str__(self): return self.full_name
    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

class Customer(models.Model):
    full_name = models.CharField(max_length=100, verbose_name="ФИО", blank=True)
    phone = models.CharField(max_length=20, unique=True, verbose_name="Телефон")
    bonus_points = models.IntegerField(default=0, verbose_name="Бонусные баллы")
    def __str__(self): return self.phone
    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Наименование")
    def __str__(self): return self.name
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория")
    name = models.CharField(max_length=100, verbose_name="Наименование")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    is_available = models.BooleanField(default=True, verbose_name="В наличии")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Фото товара")
    def __str__(self): return self.name
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары (Меню)"

class Ingredient(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование")
    unit = models.CharField(max_length=10, verbose_name="Ед. изм.")
    stock_qty = models.DecimalField(max_digits=10, decimal_places=3, default=0, verbose_name="Остаток на складе")
    def __str__(self): return self.name
    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты (Склад)"

class Recipe(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name="Ингредиент")
    amount = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Количество")
    def __str__(self): return f"{self.product.name} - {self.ingredient.name}"
    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

class Order(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name="Сотрудник")
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Клиент")
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    status = models.CharField(max_length=20, default='Новый', verbose_name="Статус")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Итоговая сумма")
    def __str__(self): return f"Заказ №{self.id}"
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Товар")
    quantity = models.IntegerField(verbose_name="Количество")
    price_at_moment = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена на момент покупки")
    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказов"

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    payment_method = models.CharField(max_length=20, verbose_name="Способ оплаты")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"

class Supplier(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование")
    contact_person = models.CharField(max_length=100, blank=True, verbose_name="Контактное лицо")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    def __str__(self): return self.name
    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"

class Supply(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, verbose_name="Поставщик")
    supply_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата поставки")
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Общая стоимость")
    def __str__(self): return f"Поставка №{self.id}"
    class Meta:
        verbose_name = "Поставка"
        verbose_name_plural = "Поставки"

class SupplyItem(models.Model):
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE, related_name='items', verbose_name="Поставка")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT, verbose_name="Ингредиент")
    quantity = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Количество")
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за единицу")
    class Meta:
        verbose_name = "Позиция поставки"
        verbose_name_plural = "Позиции поставок"