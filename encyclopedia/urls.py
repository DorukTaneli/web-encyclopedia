from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("add", views.add, name="add"),
    path("<str:name>", views.wiki, name="wiki"),
    path("edit", views.edit, name="edit")
]
