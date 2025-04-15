from rest_framework import serializers
from .models import Category,Product,Review
from django.db.models import Avg
from rest_framework.exceptions import ValidationError

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars']

    def validate_stars(self, value):
            if value < 1 or value > 5:
                raise ValidationError('Выберите от 1 до 5')


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'name', 'product_count']

    def get_product_count(self, category):
            return Product.objects.filter(category=category).count()

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise ValidationError('Категория уже существует')


class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)
    ratings = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_ratings(self, product):
        return product.reviews.aggregate(avg=Avg('stars'))['avg']

    def validate_price(self, value):
        if value <= 0:
            raise ValidationError("Цена на продукт должна быть больще нуля")
        return value

    def validate_category(self, value):
        if Category.objects.filter(name=value).exists():
            raise ValidationError("Категория с таким айди уже существует")
        return value



