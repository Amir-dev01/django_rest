from django.urls import path
from .views import CategoryList, CategoryDetail, ProductList, ProductDetail, ReviewList, ReviewDetail, \
    ProductWithReviews

urlpatterns = [
    path('api/v1/categories/', CategoryList.as_view()),
    path('api/v1/categories/<int:id>/', CategoryDetail.as_view()),
    path('api/v1/products/', ProductList.as_view()),
    path('api/v1/products/<int:id>/', ProductDetail.as_view()),
    path('api/v1/reviews/', ReviewList.as_view()),
    path('api/v1/reviews/<int:id>/', ReviewDetail.as_view()),
    path('api/v1/products/reviews/', ProductWithReviews.as_view()),

]
