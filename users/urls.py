from django.urls import path
from .views import register_api_view, login_api_view, confirm_api_view

urlpatterns = [
    path('register/', register_api_view),
    path('login/', login_api_view),
    path('confirm/', confirm_api_view),
]
