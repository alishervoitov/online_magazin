from django.contrib.auth.models import User
from django.db import models
from products.models import Product
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="Mahsulot")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name="Foydalanuvchi")
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="Reyting (1-5)")
    comment = models.TextField(blank=True, null=True, verbose_name="Izoh matni")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti")

    class Meta:
        verbose_name = "Izoh va Reyting"
        verbose_name_plural = "Izohlar va Reytinglar"
        unique_together = ('product', 'user') # Har bir foydalanuvchi bitta mahsulotga bitta izoh qoldira oladi

    def __str__(self):
        return f"{self.user.username} - {self.product.title} ({self.rating} yulduz)"


# Mahsulotning o'rtacha reytingini va izohlar sonini yangilovchi funksiya
def update_product_rating(product):
    reviews = product.reviews.all()
    if reviews.exists():
        avg_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
        product.average_rating = round(avg_rating, 1)
        product.reviews_count = reviews.count()
    else:
        product.average_rating = 0.0
        product.reviews_count = 0
    product.save()

@receiver(post_save, sender=Review)
def review_saved(sender, instance, **kwargs):
    update_product_rating(instance.product)

@receiver(post_delete, sender=Review)
def review_deleted(sender, instance, **kwargs):
    update_product_rating(instance.product)