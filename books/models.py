from django.db import models
from django.contrib.auth.models import User
from authors.models import Author

class Book(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    name_of_book = models.CharField(max_length=255)
    date_of_release = models.DateField()
    author = models.ForeignKey(Author, blank=True, null=True, on_delete=models.CASCADE)
    description = models.TextField()
    file = models.FileField(upload_to='books/', blank=True, null=True)
    cover = models.ImageField(upload_to='images/', blank=True, null=True)