from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Erkak'),
        ('F', 'Ayol'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="Foydalanuvchi")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Profil rasmi")
    phone_number = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name="Telefon raqami")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Tug'ilgan sana")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True, verbose_name="Jinsi")

    region = models.CharField(max_length=100, blank=True, null=True, verbose_name="Viloyat / Respublika")
    district = models.CharField(max_length=100, blank=True, null=True, verbose_name="Shahar / Tuman")
    address = models.TextField(blank=True, null=True, verbose_name="Aniq manzil (ko'cha, uy, xonadon)")
    postal_code = models.CharField(max_length=20, blank=True, null=True, verbose_name="Pochta indeksi")

    loyalty_points = models.PositiveIntegerField(default=0, verbose_name="Bonus ballari")
    is_verified = models.BooleanField(default=False, verbose_name="Telefon tasdiqlanganmi?")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ro'yxatdan o'tgan vaqti")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Oxirgi o'zgartirilgan vaqti")

    class Meta:
        verbose_name = "Foydalanuvchi profili"
        verbose_name_plural = "Foydalanuvchi profillari"

    def __str__(self):
        return f"{self.user.username} ({self.phone_number or 'Telefon yo\'q'})"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()