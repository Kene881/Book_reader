from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from books.models import Book

# Create your models here.
class Notes(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    num_page = models.IntegerField()
    description = models.CharField(max_length=255)