from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'price', 'quantity', 'total_item_price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'phone_number', 'total_price', 'status', 'is_paid', 'created_at')
    list_filter = ('status', 'payment_method', 'is_paid', 'created_at')
    search_fields = ('first_name', 'last_name', 'phone_number', 'user__username')
    inlines = [OrderItemInline]
    list_editable = ('status', 'is_paid')