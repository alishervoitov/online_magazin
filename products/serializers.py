from rest_framework import serializers
from .models import Category, Product, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_main']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image', 'is_active']

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    images = ProductImageSerializer(many=True, read_only=True)
    current_price = serializers.ReadOnlyField(source='get_price')

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'category_name', 'title', 'slug',
            'description', 'price', 'discount_price', 'current_price',
            'stock', 'is_available', 'is_bestseller', 'attributes',
            'images', 'created_at'
        ]