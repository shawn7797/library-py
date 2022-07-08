from dataclasses import dataclass
from django.shortcuts import render
from django.http import HttpResponse
from . models import Book, Publisher
import json
from django.views.decorators.csrf import csrf_exempt
from myapp.forms import BookForm, PublisherForm

from rest_framework.response import Response
from rest_framework.decorators import api_view
from myapp.serializers import BookSerializer, PublisherSerializer

def index(request):
    return render(request, "index.html")

def get_book(request):
    try:
        return render(request, "BookByTitle.html")
    except:
        return index

@api_view(['GET'])
def get_book_by_id(request, book_id):
    if book_id:
        try:
            book = Book.objects.get(pk=book_id)
            # return HttpResponse(f'Book {book.title} was published by {book.publisher.publisher_name} on {book.pub_date.strftime("%d/%m/%Y %H:%M:%S")}.')
            # data = { "title": book.title, "pub_date": book.pub_date.strftime("%d/%m/%Y %H:%M:%S"), "publisher": book.publisher.publisher_name }
            serializer = BookSerializer(book, many=False)
            return Response(serializer.data)
        except Book.DoesNotExist:
            return Response({})
        except:
            return Response({ 'status': 'error', 'message': 'Error occurred while querying database!' })

@api_view(['POST'])
def search_book_by_title(request):
    searched_title = str(request.POST["title"])
    print('request.POST["title"]: ', request.POST)

    if searched_title is None or searched_title == '':
        return Response({ "status": "error", "result": 'Title not defined' })
    
    try:
        book = Book.objects.get(title__icontains=searched_title)
        return Response({ "status": "success", "result": f'Book {book.title} was published by {book.publisher.publisher_name} on {book.pub_date.strftime("%d/%m/%Y %H:%M:%S")}.' })
    except Book.DoesNotExist:
        return Response({ "status": "error", "result": f'No book found with name {searched_title}' })
    except:
        return Response({ "status": "error", "result": "Error occurred!" })

def post_book_by_title(request):
    if "book_title" not in request.POST:
        return render(request, "BookByTitleResult.html", { "status": "Error!", "result": 'No Data to display' })
    
    searched_title = str(request.POST["book_title"])

    try:
        book = Book.objects.get(title__icontains=searched_title)
        return render(request, "BookByTitleResult.html", { "status": "success", "result": f'Book {book.title} was published by {book.publisher.publisher_name} on {book.pub_date.strftime("%d/%m/%Y %H:%M:%S")}.' })
    except Book.DoesNotExist:
        return render(request, "BookByTitleResult.html", { "status": "Error!", "result": f'No book found with name {searched_title}' })
    except:
        return render(request, "BookByTitleResult.html", { "status": "Error!", "result": "Error occurred!" })

@api_view(['GET'])
def get_books(request):
    try:
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    except Book.DoesNotExist:
        return Response(({ "status": "success", "message": "No books available! Please add a new book and try again."}))

@api_view(['GET'])
def get_books_view(request):
    try:
        books = Book.objects.all()
        return render(request, "AllBooksTable.html", { 'books': books })
    except Book.DoesNotExist:
        return Response({ "status": "Error", "message": "No books available! Please add a new book and try again."})

@api_view(['GET'])
def get_publishers_view(request):
    publishers = Publisher.objects.all()
    return render(request, 'AllPublishersTable.html', { 'publishers': publishers })

@api_view(['GET'])
def get_publishers(request):
    try:
        publishers = Publisher.objects.all()
        serializer = PublisherSerializer(publishers, many=True)
        return Response(serializer.data)
    except Publisher.DoesNotExist:
        return Response({ "status": "error", "message": "No Publishers found!"})

@api_view(['POST'])
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
            return Response(({ 'status': 'success' }) )
        except:
            return Response(({ 'status': 'error', 'message': 'Error occurred while adding book!' }) )
    else:
        return Response(({ 'status': 'error', 'message': 'Form data is not valid!' }) )

@api_view(['POST'])
@csrf_exempt
def add_publisher(request):
    form = PublisherForm(data=request.POST)
    if form.is_valid():
        obj = Publisher()
        obj.publisher_name = form.cleaned_data['publisher_name']
        obj.location = form.cleaned_data['location']

        try:
            obj.save()
            return Response(({ 'status': 'success' }) )
        except:
            return Response(({ 'status': 'error', 'message': 'Error occurred while adding publisher!' }) )
    else:
        return Response(({ 'status': 'error', 'message': 'Form data is not valid!' }) )

@api_view(['GET'])
def get_publisher_books(request):
    if request.GET.get('publisher_id'):
        publisher_id = int(request.GET.get('publisher_id'))
        try:
            filtered_books = Book.objects.filter(publisher=publisher_id)
            data = []
            for book in filtered_books:
                data.append({ "title": book.title, 'price': book.price, "pub_date": book.pub_date.strftime("%d/%m/%Y"), "publisher": book.publisher.publisher_name })
            return Response(({ 'books': data }) )
        except:
            return Response(({ 'status': 'error', 'message': 'Error occurred while querying database!' }) )

@api_view(['GET'])
def add_book_view(request):
    publishers = Publisher.objects.all();
    return render(request, 'AddBook.html', { 'publishers': publishers } )

@api_view(['GET'])
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
        return Response(({ 'status': 'success' }) )
    except:
        return Response(({ 'status': 'error', 'message': 'Error occurred while updating book!' }) )

@api_view(['POST'])
@csrf_exempt
def update_publisher(request):
    obj = Publisher.objects.get(pk=request.POST.get('publisher_id'))
    if request.POST.get('publisher_name') is not None:
        obj.publisher_name = request.POST.get('publisher_name')
    if request.POST.get('location') is not None:
        obj.location = request.POST.get('location')

    try:
        obj.save()
        return Response(({ 'status': 'success' }) )
    except:
        return Response(({ 'status': 'error', 'message': 'Error occurred while updating publisher!' }) )

@api_view(['POST'])
@csrf_exempt
def delete_book(request):
    try:
        obj = Book.objects.get(pk=request.POST.get('book_id'))
        obj.delete()
        return Response(({ 'status': 'success' }) )
    except Book.DoesNotExist:
        return Response(({ "status": "error", "message": "Book does not exist!"}))
    except:
        return Response(({ 'status': 'error', 'message': 'Error occurred while deleting book!' }) )

@api_view(['POST'])
@csrf_exempt
def delete_publisher(request):
    try:
        obj = Publisher.objects.get(pk=request.POST.get('publisher_id'))
        obj.delete()
        return Response(({ 'status': 'success' }) )
    except Publisher.DoesNotExist:
        return Response(({ "status": "error", "message": "Publisher does not exist!"}))
    except:
        return Response(({ 'status': 'error', 'message': 'Error occurred while deleting publisher!' }) )

@api_view(['GET'])
def delete_book_view(request):
    books = Book.objects.all()
    return render(request, 'DeleteBook.html', { 'books': books })

@api_view(['GET'])
def delete_publisher_view(request):
    publishers = Publisher.objects.all()
    return render(request, 'DeletePublisher.html', { 'publishers': publishers })

