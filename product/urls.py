from django.urls import path
from .views import *

urlpatterns = [
    path('categories/', category_list),
    path('categories/<int:id>/', category_detail),

    path('products/', product_list),
    path('products/<int:id>/', product_detail),

    path('reviews/', review_list),

    path('products-with-reviews/', products_with_reviews),
    path('categories-with-count/', categories_with_count),
]
