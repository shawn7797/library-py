from django.shortcuts import render
from django.http import HttpResponse
from . models import Book, Publisher
import json

def index(request):
    return HttpResponse("Hello World")

def book_by_id(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return HttpResponse("No Book was found!")
    book = Book.objects.get(pk=book_id)
    # return HttpResponse(f'Book {book.title} was published by {book.publisher.publisher_name} on {book.pub_date.strftime("%d/%m/%Y %H:%M:%S")}.')
    data = { "title": book.title, "pub_date": book.pub_date.strftime("%d/%m/%Y %H:%M:%S"), "publisher": book.publisher.publisher_name }
    return HttpResponse( json.dumps( data ) )

def get_books(request):
    try:
        books = Book.objects.all()
    except Book.DoesNotExist:
        return HttpResponse({ "status": "Error", "message": "No books available! Please add a new book and try again."})
    books = Book.objects.all()
    books_list = []
    for book in books:
        books_list.append({ "title": book.title, "pub_date": book.pub_date.strftime("%d/%m/%Y %H:%M:%S"), "publisher": book.publisher.publisher_name })
    return HttpResponse( json.dumps( books_list ) )

def get_publishers(request):
    try:
        books = Publisher.objects.all()
    except Publisher.DoesNotExist:
        return HttpResponse({ "status": "Error", "message": "No Publishers found!"})
    publishers = Publisher.objects.all()
    publishers_list = []
    for publisher in publishers:
        publishers_list.append({ "name": publisher.publisher_name, "location": publisher.location })
    return HttpResponse( json.dumps( publishers_list ) )
