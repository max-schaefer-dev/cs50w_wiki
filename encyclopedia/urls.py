from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<title>", views.entry, name="entry"),
    path("random", views.random_entry, name="random-entry"),
    path("new-entry", views.new_entry, name="new-entry"),
    path("?q=<title>", views.entry)
]
