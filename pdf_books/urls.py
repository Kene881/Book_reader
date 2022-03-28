from django.urls import path
from . import views

app_name = 'pdf_books'

urlpatterns = [
    path('<int:id>/', views.get_book, name='get_book'),
    path('create/<int:id>/', views.create, name='create_note'),
    path('delete/<int:id>/', views.delete, name='delete_note'),
    path('download/<int:id>/', views.download_book, name='download_book')
]