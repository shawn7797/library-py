from django.shortcuts import render
from django.http import HttpResponse
from . models import Book, Publisher
import json

def index(request):
    return render(request, "index.html")

def get_book(request):
    try:
        return render(request, "BookByTitle.html")
    except:
        return index

def get_book_by_id(request, book_id):
    if book_id:
        try:
            book = Book.objects.get(pk=book_id)
            # return HttpResponse(f'Book {book.title} was published by {book.publisher.publisher_name} on {book.pub_date.strftime("%d/%m/%Y %H:%M:%S")}.')
            data = { "title": book.title, "pub_date": book.pub_date.strftime("%d/%m/%Y %H:%M:%S"), "publisher": book.publisher.publisher_name }
            return HttpResponse(json.dumps(data))
        except Book.DoesNotExist:
            return HttpResponse(json.dumps({ 'status': 'success', 'result': {} }))
        except:
            return HttpResponse(json.dumps({ 'status': 'error', 'message': 'Error occurred while querying database!' }))

def post_book_by_title(request):
    if "book_title" not in request.POST:
        return render(request, "BookByTitleResult.html", { "status": "Error!", "result": 'No Data to display' })
    
    searched_title = str(request.POST["book_title"])

    try:
        book = Book.objects.get(title__icontains=searched_title)
        print('book = Book.objects.get(name__icontains=searched_title): ', Book.objects.get(title__icontains=searched_title))
        return render(request, "BookByTitleResult.html", { "status": "Success!", "result": f'Book {book.title} was published by {book.publisher.publisher_name} on {book.pub_date.strftime("%d/%m/%Y %H:%M:%S")}.' })
    except Book.DoesNotExist:
        return render(request, "BookByTitleResult.html", { "status": "Error!", "result": f'No book found with name {searched_title}' })
    except:
        return render(request, "BookByTitleResult.html", { "status": "Error!", "result": "Error occurred!" })

def get_books(request):
    try:
        books = Book.objects.all()
    except Book.DoesNotExist:
        return HttpResponse({ "status": "Error", "message": "No books available! Please add a new book and try again."})
    books = Book.objects.all()
    return render(request, "AllBooksTable.html", { 'books': books })

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
