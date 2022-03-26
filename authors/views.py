from django.shortcuts import render, redirect
from .forms import AuthorForm
from .models import Author

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect('books:get-obj')
    if not request.user.is_staff:
        return redirect('books:get-obj')
    authors = Author.objects.all()
    form = AuthorForm()
    return render(request, 'authors/index.html', { 'authors': authors, 'form': form })

def create(request):
    if not request.user.is_authenticated:
        return redirect('books:get-obj')
    if not request.user.is_staff:
        return redirect('books:get-obj')
    form = AuthorForm(request.POST)
    if form.is_valid():
        form.save()
    return redirect('authors:index')

def delete(request, id):
    if not request.user.is_authenticated:
        return redirect('books:get-obj')
    if not request.user.is_staff:
        return redirect('books:get-obj')
    author = Author.objects.get(pk=id)
    author.delete()
    return redirect('authors:index')