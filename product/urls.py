from django.urls import path
from .views import *

urlpatterns = [
    path('categories/', category_list),
    path('categories/<int:id>/', category_detail),

    path('products/', product_list),
    path('products/<int:id>/', product_detail),

    path('reviews/', review_list),
    path('reviews/<int:id>/', review_detail),
]
