from django.urls import path
from .views import (
    CategoryListCreateView, CategoryRetrieveUpdateDestroyView,
    ProductListCreateView, ProductRetrieveUpdateDestroyView,
    ReviewListCreateView, ReviewRetrieveUpdateDestroyView,
    ProductWithReviewsView
)

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view()),
    path('categories/<int:id>/', CategoryRetrieveUpdateDestroyView.as_view()),

    path('products/', ProductListCreateView.as_view()),
    path('products/<int:id>/', ProductRetrieveUpdateDestroyView.as_view()),

    path('reviews/', ReviewListCreateView.as_view()),
    path('reviews/<int:id>/', ReviewRetrieveUpdateDestroyView.as_view()),

    path('products-with-reviews/', ProductWithReviewsView.as_view()),
]