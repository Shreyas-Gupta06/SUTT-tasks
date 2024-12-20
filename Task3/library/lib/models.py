# lib/models.py
from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    published_date = models.DateField()
    isbn_number = models.CharField(max_length=13, unique=True)  # ISBN number
    available_copies = models.IntegerField(default=1)  # Available copies in the library

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