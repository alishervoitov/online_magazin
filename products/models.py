from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Kategoriya nomi")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="Slug")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="Kategoriya rasmi")
    is_active = models.BooleanField(default=True, verbose_name="Faolligi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti")

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name