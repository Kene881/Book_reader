from django.db import models

# Create your models here.
class Author(models.Model):
    # portrait
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'