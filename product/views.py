from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category,Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer


class CategoryList(APIView):
    def get(self,request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetail(APIView):
    def get(self, request, id):
        category = get_object_or_404(Category, id=id)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def delete(self, request, id):
        category = get_object_or_404(Category, id=id)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductList(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, id=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def delete(self, request, id):
        product = get_object_or_404(Product, id=id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ReviewList(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewDetail(APIView):
    def get(self, request, id):
        review = get_object_or_404(Review, id=id)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    def delete(self, request, id):
        review = get_object_or_404(Review, id=id)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductWithReviews(APIView):
    def get(self, request):

        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)



@api_view(['GET', 'POST'])
def category_list_api_view(request):
    if request.method == 'GET':
        categories = Category.objects.annotate(product_count=Count('product'))
        data = CategorySerializer(categories, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        name = request.data.get('name')
        category = Category.objects.create(name=name)
        # вручную добавляем product_count = 0 при создании
        category.product_count = 0
        return Response(CategorySerializer(category).data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.annotate(product_count=Count('product')).get(id=id)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(CategorySerializer(category).data)

    elif request.method == 'PUT':
        category.name = request.data.get('name')
        category.save()
        category.product_count = category.product_set.count()
        return Response(CategorySerializer(category).data, status=status.HTTP_200_OK)

    else:
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def product_list_api_view(request):
    if request.method == 'GET':
        products = Product.objects.prefetch_related('reviews')
        data = ProductSerializer(products, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        product = Product.objects.create(
            name=request.data.get('name'),
            description=request.data.get('description'),
            price=request.data.get('price'),
            category_id=request.data.get('category')
        )
        data = ProductSerializer(product).data
        return Response(data=data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.prefetch_related('reviews').get(id=id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(ProductSerializer(product).data)

    elif request.method == 'PUT':
        product.name = request.data.get('name')
        product.description = request.data.get('description')
        product.price = request.data.get('price')
        product.category_id = request.data.get('category')
        product.save()
        return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)

    else:
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data = ReviewSerializer(reviews, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        review = Review.objects.create(
            product_id=request.data.get('product'),
            text=request.data.get('text'),
            stars=request.data.get('stars'),
        )
        data = ReviewSerializer(review).data
        return Response(data=data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(ReviewSerializer(review).data)

    elif request.method == 'PUT':
        review.text = request.data.get('text')
        review.stars = request.data.get('stars')
        review.save()
        return Response(ReviewSerializer(review).data, status=status.HTTP_200_OK)

    else:
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)