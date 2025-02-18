# lib/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    published_date = models.DateField()
    isbn_number = models.BigIntegerField(unique=True)
    available_copies = models.IntegerField(
    validators=[MinValueValidator(0)]
)
    image = models.ImageField(upload_to='book_images/', blank=True, null=True)  # Add this line
    total_ratings = models.IntegerField(default=0)
    total_rating_value = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
    @property
    def average_rating(self):
        if self.total_ratings > 0:
            return self.total_rating_value / self.total_ratings
        return 0



class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=20, blank=True, null=True)
    hostel = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username

class LibrarianProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    psrn_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
class Borrow(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issued_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    late_fees = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    

class GlobalSettings(models.Model):
    issue_period = models.IntegerField(default=7)
    late_fees_per_day = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)


class Feedback(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    image = models.ImageField(upload_to='feedback_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
    

class BookRating(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()
    date_rated = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'book')


class BorrowedHistory(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issued_date = models.DateField()
    return_date = models.DateField()

    def __str__(self):
        return f"{self.student.user.username} - {self.book.title}"