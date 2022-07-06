from dataclasses import dataclass
from django.shortcuts import render
from django.http import HttpResponse
from . models import Book, Publisher
import json
from django.views.decorators.csrf import csrf_exempt
from myapp.forms import BookForm, PublisherForm

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

@csrf_exempt
def add_book(request):
    form = BookForm(data=request.POST)
    if form.is_valid():
        obj = Book()
        obj.title = form.cleaned_data['title']
        obj.price = form.cleaned_data['price']
        obj.pub_date = form.cleaned_data['pub_date']

        publisher = Publisher.objects.get(pk=form.cleaned_data['publisher'])
        obj.publisher = publisher
        try:
            obj.save()
            return HttpResponse( json.dumps({ 'status': 'success' }) )
        except:
            return HttpResponse( json.dumps({ 'status': 'error', 'message': 'Error occurred while adding book!' }) )
    else:
        return HttpResponse( json.dumps({ 'status': 'error', 'message': 'Form data is not valid!' }) )

@csrf_exempt
def add_publisher(request):
    form = PublisherForm(data=request.POST)
    if form.is_valid():
        obj = Publisher()
        obj.publisher_name = form.cleaned_data['publisher_name']
        obj.location = form.cleaned_data['location']

        try:
            obj.save()
            return HttpResponse( json.dumps({ 'status': 'success' }) )
        except:
            return HttpResponse( json.dumps({ 'status': 'error', 'message': 'Error occurred while adding publisher!' }) )
    else:
        return HttpResponse( json.dumps({ 'status': 'error', 'message': 'Form data is not valid!' }) )

def get_publisher_books(request):
    if request.GET.get('publisher_id'):
        publisher_id = int(request.GET.get('publisher_id'))
        try:
            filtered_books = Book.objects.filter(publisher=publisher_id)
            data = []
            for book in filtered_books:
                data.append({ "title": book.title, 'price': book.price, "pub_date": book.pub_date.strftime("%d/%m/%Y"), "publisher": book.publisher.publisher_name })
            return HttpResponse( json.dumps({ 'books': data }) )
        except:
            return HttpResponse( json.dumps({ 'status': 'error', 'message': 'Error occurred while querying database!' }) )

def add_book_view(request):
    publishers = Publisher.objects.all();
    return render(request, 'AddBook.html', { 'publishers': publishers } )

def add_publisher_view(request):
    return render(request, 'AddPublisher.html' )

@csrf_exempt
def update_book(request):
    obj = Book.objects.get(pk=request.POST.get('book_id'))
    if request.POST.get('title') is not None:
        obj.title = request.POST.get('title')
    if request.POST.get('price') is not None:
        obj.price = request.POST.get('price')
    if request.POST.get('pub_date') is not None:
        obj.pub_date = request.POST.get('pub_date')
    if request.POST.get('publisher') is not None:
        publisher = Publisher.objects.get(pk=request.POST.get('publisher'))
        obj.publisher = publisher

    try:
        obj.save()
        return HttpResponse( json.dumps({ 'status': 'success' }) )
    except:
        return HttpResponse( json.dumps({ 'status': 'error', 'message': 'Error occurred while updating book!' }) )


@csrf_exempt
def update_publisher(request):
    obj = Publisher.objects.get(pk=request.POST.get('publisher_id'))
    if request.POST.get('publisher_name') is not None:
        obj.publisher_name = request.POST.get('publisher_name')
    if request.POST.get('location') is not None:
        obj.location = request.POST.get('location')

    try:
        obj.save()
        return HttpResponse( json.dumps({ 'status': 'success' }) )
    except:
        return HttpResponse( json.dumps({ 'status': 'error', 'message': 'Error occurred while updating publisher!' }) )