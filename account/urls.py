from django.urls import path
from . import views


urlpatterns = [

path('', views.home, name='home'),

path('register/', views.register_user, name='register'),
path('verify-otp/', views.verify_email_otp, name='verify-otp'),

path('login/', views.login_user, name='login'),
path('logout/', views.logout_user, name='logout'),

path('profile/', views.profile, name='profile'),
path('update-profile/', views.update_profile, name='update-profile'),
path('upload-avatar/', views.upload_avatar, name='upload-avatar'),

path('password-reset/', views.password_reset_request, name='password-reset-request'),
path('password-reset-verify/', views.password_reset_verify_otp, name='password-reset-verify'),
path('password-reset-confirm/', views.password_reset_confirm, name='password-reset-confirm'),

]