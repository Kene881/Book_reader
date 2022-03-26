from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.db import transaction
from books.models import Book
from authors.models import Author
from .forms import BookForm

def get(request):
    books = Book.objects.all()
    return render(request, 'books/index.html', { 'books': books })

def get_detail(request, id):
    book = Book.objects.get(pk=id)
    return render(request, 'books/detail.html', { 'book': book })

@transaction.atomic
def update(request, id):
    book = Book.objects.get(pk=id)

    if not request.user.is_authenticated:
        return redirect('books:get-obj')
    if not book.user == request.user:
        return redirect('books:get-obj')

    if request.method == 'POST':
        cover = request.POST.get('cover')
        file = request.POST.get('file')
        author = request.POST.get('author')

        if author != '':
            book.author = Author.objects.get(pk=author)    
        if file != '':
            book.file = request.FILES['file']
        if cover != '':
            book.cover = request.FILES['cover']
        
        book.name_of_book = request.POST.get('name_of_book')
        book.date_of_release = request.POST.get('date_of_release')
        book.description = request.POST.get('description')
        
        book.save()

        return redirect('books:get-one-obj', id=id)
    else:
        form = BookForm(initial={
                    'name_of_book': book.name_of_book, 
                    'date_of_release': book.date_of_release, 
                    'description': book.description,
                    'author': book.author,
                }
            )
    
    return render(request, 'books/update.html', { 'form': form, 'book_id': id })

@transaction.atomic
def create(request):
    if not request.user.is_authenticated:
        return redirect('books:get-obj')

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.save()
            return redirect('books:get-obj')
    else:
        form = BookForm()
        
    return render(request, 'books/create.html', { 'form': form })

@transaction.atomic
def delete(request, id):
    book = Book.objects.get(pk = id)
    
    if not book.user == request.user:
        return redirect('books:get-obj')
    if not request.user.is_authenticated:
        return redirect('books:get-obj')
    
    book.delete()
    return redirect('books:get-obj')