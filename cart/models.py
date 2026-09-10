from django.contrib.auth.models import User
from django.db import models
from products.models import Product

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', verbose_name="Foydalanuvchi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti")

    class Meta:
        verbose_name = "Savatcha"
        verbose_name_plural = "Savatchalar"

    def __str__(self):
        return f"{self.user.username} ning savatchasi"

    @property
    def total_price(self):
        return sum(item.total_item_price for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE, verbose_name="Savatcha")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Mahsulot")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Soni")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Savatcha elementi"
        verbose_name_plural = "Savatcha elementlari"

    def __str__(self):
        return f"{self.product.title} ({self.quantity} dona)"

    @property
    def total_item_price(self):
        price = self.product.discount_price if self.product.discount_price else self.product.price
        return price * self.quantity