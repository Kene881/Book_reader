from django.shortcuts import redirect, render
from django.http import HttpResponse
from books.models import Book
from authors.models import Author
from .forms import BookForm

cyrillic = {
    'а': 'a', 'А': 'a',
    'б': 'b', 'Б': 'b', 
    'в': 'v', 'В': 'v', 
    'г': 'g', 'Г': 'g',
    'д': 'd', 'Д': 'd',
    'е': 'e', 'Е': 'e',
    'ё': 'e', 'Ё': 'e', 
    'ж': 'zh', 'Ж': 'zh',
    'з': 'z', 'З': 'z', 
    'и': 'i', 'И': 'i',
    'й': 'i', 'Й': 'i',
    'к': 'k', 'К': 'k', 
    'л': 'l', 'Л': 'l',
    'м': 'm', 'М': 'm',
    'н': 'n', 'Н': 'n',
    'о': 'o', 'О': 'o', 
    'п': 'p', 'П': 'p', 
    'р': 'r', 'Р': 'r', 
    'с': 's', 'С': 's',
    'т': 't', 'Т': 't',
    'у': 'u', 'У': 'u', 
    'ф': 'f', 'Ф': 'f', 
    'х': 'h', 'Х': 'h', 
    'ц': 'ts', 'Ц': 'ts', 
    'ч': 'ch', 'Ч': 'ch',
    'ш': 'sh', 'Ш': 'sh', 
    'щ': 'sh', 'Щ': 'sh', 
    'ъ': '', 'Ъ': '', 
    'ь': '', 'Ь': '', 
    'ы': 'i', 'Ы': 'i',
    'э': 'e', 'Э': 'e', 
    'ю': 'yu', 'Ю': 'yu',
    'я': 'ya', 'Я': 'ya',
}

def change_char(word):
    new_word = ''
    
    for i in word:
        char = i
        if i in cyrillic.keys():
            char = cyrillic[i]
        new_word += char
    
    return new_word

def get(request):
    books = Book.objects.all()
    return render(request, 'books/index.html', { 'books': books })

def get_detail(request, id):
    book = Book.objects.get(pk=id)
    return render(request, 'books/detail.html', { 'book': book })

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
            request.FILES['file'].name = change_char(request.FILES['file'].name)
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

def create(request):
    if not request.user.is_authenticated:
        return redirect('books:get-obj')

    if request.method == 'POST':
        
        request.FILES['file'].name = change_char(request.FILES['file'].name)

        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.save()
            return redirect('books:get-obj')
    else:
        form = BookForm()
        
    return render(request, 'books/create.html', { 'form': form })

def delete(request, id):
    book = Book.objects.get(pk = id)
    
    if not book.user == request.user:
        return redirect('books:get-obj')
    if not request.user.is_authenticated:
        return redirect('books:get-obj')
    
    book.delete()
    return redirect('books:get-obj')