from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (ChangeUserPassword, LoginUserView, ProfileOrdersView,
                    ProfileView, RegisterUserView)

urlpatterns = [
    path('<int:pk>/profile/', ProfileView.as_view(), name='profile'),
    path('orders/', ProfileOrdersView.as_view(), name='orders'),
    path('profile/change_password/', ChangeUserPassword.as_view(), name='change-password'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),

]
