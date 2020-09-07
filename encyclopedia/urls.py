from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<title>", views.entry, name="entry"),
    path("new_page", views.new_page, name="new-page"),
    path("?q=<title>", views.entry)
]
