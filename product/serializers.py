from rest_framework import serializers
from .models import Category,Product,Review
from django.db.models import Avg

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars']


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'name', 'product_count']

    def get_product_count(self, category):
            return Product.objects.filter(category=category).count()


class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)
    ratings = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_ratings(self, product):
        return product.reviews.aggregate(avg=Avg('stars'))['avg']

