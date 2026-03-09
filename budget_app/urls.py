from django.urls import path
from . import views

urlpatterns = [

    path("categories/", views.categories_page),
    path("categories/create/", views.create_category),
    path("categories/list/", views.list_categories),
    path("categories/delete/<int:pk>/", views.delete_category),

    path("", views.budget_page),
    path("create/", views.create_budget),
    path("list/", views.list_budgets),
    path("delete/<int:pk>/", views.delete_budget),
    path("edit/<int:pk>/", views.edit_budget),

    path("utilization/", views.budget_utilization),
]