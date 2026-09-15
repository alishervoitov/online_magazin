from rest_framework import serializers
from .models import Review
from products.models import Product

class ReviewSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = Review
        fields = ['id', 'product_id', 'user_username', 'rating', 'comment', 'created_at']
        read_only_fields = ['user_username', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        product = validated_data['product']

        # Agar foydalanuvchi bu mahsulotga oldin izoh yozgan bo'lsa, uni yangilaymiz yoki xato beramiz
        review, created = Review.objects.update_or_create(
            user=user,
            product=product,
            defaults={
                'rating': validated_data['rating'],
                'comment': validated_data.get('comment', '')
            }
        )
        return review