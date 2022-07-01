import imp
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("get_book/<int:book_id>", views.book_by_id, name="get_book_by_id"),
    path("get_books", views.get_books, name="get_books"),
    path("get_publishers", views.get_publishers, name="get_publishers")
]
