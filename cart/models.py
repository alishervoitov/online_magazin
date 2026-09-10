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