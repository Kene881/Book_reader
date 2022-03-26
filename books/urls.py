from django.urls import path
from books import views

app_name = 'books'

urlpatterns = [
    path('create/', views.create, name='create-obj'),
    path('', views.get, name='get-obj'),
    path('<int:id>/', views.get_detail, name='get-one-obj'),
    path('delete/<int:id>/', views.delete, name='delete-obj'),
    path('update/<int:id>/', views.update, name='update-obj')
]