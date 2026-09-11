from django.contrib.auth.models import User
from django.db import models
from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Kutishda'),
        ('confirmed', 'Tasdiqlangan'),
        ('on_the_way', 'Yo\'lda'),
        ('delivered', 'Yetkazib berilgan'),
        ('cancelled', 'Bekor qilingan'),
    )

    PAYMENT_CHOICES = (
        ('cash', 'Naqd pul orqali'),
        ('click', 'Click / Payme'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="Foydalanuvchi")

    # Yetkazib berish ma'lumotlari
    first_name = models.CharField(max_length=100, verbose_name="Ism")
    last_name = models.CharField(max_length=100, verbose_name="Familiya")
    phone_number = models.CharField(max_length=20, verbose_name="Telefon raqami")
    region = models.CharField(max_length=100, verbose_name="Viloyat")
    district = models.CharField(max_length=100, verbose_name="Tuman / Shahar")
    address = models.TextField(verbose_name="Aniq manzil")

    # Moliyaviy va holat ma'lumotlari
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Umumiy summa")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Buyurtma holati")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cash',
                                      verbose_name="To'lov turi")
    is_paid = models.BooleanField(default=False, verbose_name="To'langanmi?")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Buyurtma berilgan vaqti")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqti")

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
        ordering = ['-created_at']

    def __str__(self):
        return f"Buyurtma #{self.id} - {self.first_name} {self.last_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="Buyurtma")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name="Mahsulot")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Sotib olingan narxi")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Soni")

    class Meta:
        verbose_name = "Buyurtma elementi"
        verbose_name_plural = "Buyurtma elementlari"

    def __str__(self):
        product_title = self.product.title if self.product else "O'chirilgan mahsulot"
        return f"{product_title} ({self.quantity} dona)"

    @property
    def total_item_price(self):
        return self.price * self.quantity