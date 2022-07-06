import imp
from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("get_book", views.get_book, name="get_book"),
    path("get_book_by_id/<int:book_id>", views.get_book_by_id, name="get_book_by_id"),
    path("get_books", views.get_books, name="get_all_books"),
    path("get_publishers", views.get_publishers, name="get_publishers"),
    path("post_book_by_title", views.post_book_by_title, name="post_book_by_title"),
    path("add_book", views.add_book, name="add_book"),
    path("add_book_view", views.add_book_view, name="add_book_view"),
    path("add_publisher", views.add_publisher, name="add_publisher"),
    path("add_publisher_view", views.add_publisher_view, name="add_publisher_view"),
    path("get_publisher_books", views.get_publisher_books, name="get_publisher_books"),
    path("update_book", views.update_book, name="update_book"),
    path("update_publisher", views.update_publisher, name="update_publisher"),
]
