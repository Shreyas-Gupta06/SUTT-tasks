# lib/forms.py
from django import forms
from .models import StudentProfile
from .models import LibrarianProfile, Book


class ProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['room_number', 'hostel']

class LibrarianProfileForm(forms.ModelForm):
    class Meta:
        model = LibrarianProfile
        fields = ['psrn_number', 'name']

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'published_date', 'isbn_number', 'available_copies', 'image'] 