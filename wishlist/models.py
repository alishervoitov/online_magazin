from django.contrib.auth.models import User
from django.db import models
from products.models import Product

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist', verbose_name="Foydalanuvchi")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Mahsulot")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan vaqti")

    class Meta:
        verbose_name = "Sevimlilar"
        verbose_name_plural = "Sevimlilar ro'yxati"
        unique_together = ('user', 'product') # Bitta mahsulotni ikki marta qo'shib bo'lmasligi uchun

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"