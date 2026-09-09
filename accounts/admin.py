from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profil maʼlumotlari'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_phone', 'is_staff')

    def get_phone(self, obj):
        return obj.profile.phone_number
    get_phone.short_description = 'Telefon raqami'

admin.site.unregister(User)
admin.site.register(User, UserAdmin)