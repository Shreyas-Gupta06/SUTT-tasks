# lib/models.py
from django.db import models
from django.contrib.auth.models import User


from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    published_date = models.DateField()
    isbn_number = models.CharField(max_length=13, unique=True)
    available_copies = models.IntegerField()
    image = models.ImageField(upload_to='book_images/', blank=True, null=True)  # Add this line

    def __str__(self):
        return self.title




class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=20, blank=True, null=True)
    hostel = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username

class LibrarianProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    psrn_number = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username