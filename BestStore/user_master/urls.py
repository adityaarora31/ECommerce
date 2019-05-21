from django.urls import path
from .views import register_user, user_login, verify_user
from .views import register_user, user_login, logout_view, user_dashboard, forgot_pass

urlpatterns = [
    path('register/', register_user, name='register_post'),
    path('login/', user_login, name='user_login'),
    path('verify/<str:token>/', verify_user, name='user_verify'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', user_dashboard, name='dashboard'),
    # path('forgot_pass', forgot_pass, name='forgot_pass')
]
