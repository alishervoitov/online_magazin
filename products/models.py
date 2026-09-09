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


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE,
                                 verbose_name="Kategoriyasi")
    title = models.CharField(max_length=255, verbose_name="Mahsulot nomi")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Batafsil tavsifi")

    # Narx va chegirmalar
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Asosiy narxi")
    discount_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True,
                                         verbose_name="Chegirma narxi")

    # Ombor va holati
    stock = models.PositiveIntegerField(default=0, verbose_name="Ombordagi soni")
    is_available = models.BooleanField(default=True, verbose_name="Sotuvda bormi?")
    is_bestseller = models.BooleanField(default=False, verbose_name="Xit savdo / Ommabop")

    # Qo'shimcha xarakteristikalar (JSON formatida har xil xususiyatlar uchun, masalan: rang, o'lcham)
    attributes = models.JSONField(blank=True, null=True, verbose_name="Xususiyatlari (JSON)")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan vaqti")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan vaqti")

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            # Slug takrorlanib qolmasligi uchun unikal qilamiz
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def get_price(self):
        """Agar chegirma narxi bo'lsa shuni qaytaradi, aks holda asosiy narxni"""
        return self.discount_price if self.discount_price else self.price

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE, verbose_name="Mahsulot")
    image = models.ImageField(upload_to='products/', verbose_name="Rasm")
    is_main = models.BooleanField(default=False, verbose_name="Asosiy rasmmi?")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Mahsulot rasmi"
        verbose_name_plural = "Mahsulot rasmlari"

    def __str__(self):
        return f"{self.product.title} - rasm"