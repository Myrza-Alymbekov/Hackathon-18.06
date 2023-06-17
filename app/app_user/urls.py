from django.contrib.auth.views import LogoutView
from django.urls import path

from global_login_required import login_not_required

from . import views

urlpatterns = [
    path('register/', login_not_required(views.UserCreateView.as_view()), name='register'),
    path('login/', login_not_required(views.UserLoginView.as_view()), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('change_password/', login_not_required(views.PasswordUpdateView.as_view()), name='password_change'),
    path('password-reset/', login_not_required(views.PasswordEmailView.as_view()), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', login_not_required(views.PasswordResetAccView.as_view()),
         name='password_reset_confirm'),
]