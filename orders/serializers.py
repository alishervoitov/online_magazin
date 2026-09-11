from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer
from cart.models import Cart


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total_item_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'price', 'quantity', 'total_item_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'first_name', 'last_name', 'phone_number',
            'region', 'district', 'address', 'total_price',
            'status', 'payment_method', 'is_paid', 'items', 'created_at'
        ]
        read_only_fields = ['total_price', 'status', 'is_paid', 'user']

    def create(self, validated_data):
        user = self.context['request'].user

        # Foydalanuvchi savatchasini tekshiramiz
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            raise serializers.ValidationError("Savatchangiz bo'sh.")

        cart_items = cart.items.all()
        if not cart_items.exists():
            raise serializers.ValidationError("Savatchada mahsulotlar mavjud emas.")

        # Ombor qoldig'ini tekshirish va umumiy summani hisoblash
        total_price = 0
        for cart_item in cart_items:
            product = cart_item.product
            if product.stock < cart_item.quantity:
                raise serializers.ValidationError(
                    f"'{product.title}' mahsulotidan omborda yetarli miqdor yo'q.Qoldiq: {product.stock}")

            price = product.discount_price if product.discount_price else product.price
            total_price += price * cart_item.quantity

        # Buyurtmani yaratish
        order = Order.objects.create(user=user, total_price=total_price, **validated_data)

        # Savatchadagi mahsulotlarni OrderItem ga ko'chirish va omborni kamaytirish
        for cart_item in cart_items:
            product = cart_item.product
            price = product.discount_price if product.discount_price else product.price

            OrderItem.objects.create(
                order=order,
                product=product,
                price=price,
                quantity=cart_item.quantity
            )

            # Ombordan ayiramiz
            product.stock -= cart_item.quantity
            product.save()

        # Buyurtma berilgandan keyin savatchani tozalaymiz
        cart_items.delete()

        return order