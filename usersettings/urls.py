from django.urls import path
from . import views

urlpatterns = [
    path("", views.settings_page, name="settings"),
    path("get/", views.get_user_settings, name="get_user_settings"),
    path("update/", views.update_user_settings, name="update_user_settings"),
]