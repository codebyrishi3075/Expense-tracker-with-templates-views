from django.urls import path
from . import views

urlpatterns = [

    path("", views.dashboard_page, name="dashboard"),
    path("summary/", views.dashboard_summary, name="dashboard_summary"),

]