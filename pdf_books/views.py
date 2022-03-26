from django.http import HttpResponse
from django.shortcuts import redirect, render
from books.models import Book
from .forms import NoteForm
from .models import Notes

def get_book(request, id):
    if not request.user.is_authenticated:
        return redirect('books:get-obj')
    notes = Notes.objects.filter(user=request.user)
    book = Book.objects.get(pk = id)
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
    pass