from django.urls import path
from .views import register, Login, Auth

urlpatterns = [
    path('register/', register),
    path('login/', Login.as_view(), name="login"),
    path('auth/', Auth.as_view(), name="auth")
]
