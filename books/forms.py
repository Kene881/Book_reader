from django import forms
from books.models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['user', 'name_of_book', 'date_of_release', 'author', 'description', 'file', 'cover']