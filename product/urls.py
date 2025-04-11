from django.urls import path
from .views import CategoryList, CategoryDetail, ProductList, ProductDetail, ReviewList, ReviewDetail, \
    ProductWithReviews, category_list_api_view, category_detail_api_view, product_list_api_view, \
    product_detail_api_view, review_list_api_view, review_detail_api_view

urlpatterns = [
    path('api/v1/categories/', CategoryList.as_view()),
    path('api/v1/categories/<int:id>/', CategoryDetail.as_view()),
    path('api/v1/products/', ProductList.as_view()),
    path('api/v1/products/<int:id>/', ProductDetail.as_view()),
    path('api/v1/reviews/', ReviewList.as_view()),
    path('api/v1/reviews/<int:id>/', ReviewDetail.as_view()),
    path('api/v1/products/reviews/', ProductWithReviews.as_view()),

# Category endpoints
    path('api/v1/categories/', category_list_api_view),
    path('api/v1/categories/<int:id>/', category_detail_api_view),

    # Product endpoints
    path('api/v1/products/', product_list_api_view),
    path('api/v1/products/<int:id>/', product_detail_api_view),

    # Review endpoints
    path('api/v1/reviews/', review_list_api_view),
    path('api/v1/reviews/<int:id>/', review_detail_api_view),

]
