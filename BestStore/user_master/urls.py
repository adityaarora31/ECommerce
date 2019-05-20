from django.urls import path
from .views import register_user, user_login

urlpatterns = [
    path('register/', register_user, name='register_post'),
    path('login/', user_login, name='user_login')
]
