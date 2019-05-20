from django.urls import path, include
from .views import home, register, render_login_form
urlpatterns = [
    path('', home, name="homepage"),
    path('register', register, name="register"),
    path('login/', render_login_form, name="loginform"),
    path('', include('social_django.urls', namespace='social')),
]
