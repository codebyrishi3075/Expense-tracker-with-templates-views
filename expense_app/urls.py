from django.urls import path
from . import views

urlpatterns = [

path("", views.expenses_page),
path("create/", views.create_expense),
path("list/", views.list_expenses),
path("update/<int:pk>/", views.update_expense),
path("delete/<int:pk>/", views.delete_expense),

]