from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from books.models import Book
from reader_books_website.settings import BASE_DIR
from .forms import NoteForm
from .models import Notes
import os
import mimetypes

def download_book(request, id):
    book = Book.objects.get(pk=id)
    file_path = book.file.url.replace('/', "\\")
    file_path = f'{BASE_DIR}{file_path}'
    print(file_path)
    if os.path.exists(file_path):
        print('exist')
        with open(file_path, 'rb') as fl:
            response = HttpResponse(fl.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    return redirect('books:get-obj')

def get_book(request, id):
    if not request.user.is_authenticated:
        return redirect('books:get-obj')
    book = Book.objects.get(pk = id)
    notes = Notes.objects.filter(user=request.user, book=book)
    form = NoteForm()
    return render(request, 'pdf_books/reader.html', 
    { 
        'book': book, 
        'form': form,
        'notes': notes
    })

def create(request, id):
    if not request.user.is_authenticated:
        return redirect('books:get-obj')
    form = NoteForm(request.POST)
    if form.is_valid():
        form = form.save(commit=False)
        form.user = request.user
        form.book = Book.objects.get(pk=id)
        form.save()
    return redirect('pdf_books:get_book', id=id)


def delete(request, id):
    if not request.user.is_authenticated:
        return redirect('books:get-obj')
    
    note = Notes.objects.get(pk=id)

    if not note.user == request.user:
        return redirect('books:get-obj')
    
    note.delete()
    return redirect('pdf_books:get_book', id=note.book.id)