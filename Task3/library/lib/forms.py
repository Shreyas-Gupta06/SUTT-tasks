# lib/forms.py
from django import forms
from .models import StudentProfile
from .models import LibrarianProfile, Book, GlobalSettings, Feedback, BookRating


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
        
class LateFeesForm(forms.Form):
    late_fees = forms.DecimalField(label='Late Fees per Day', decimal_places=2) 



class IssuePeriodForm(forms.Form):
    issue_period = forms.IntegerField(label='Issue Period (in days)', min_value=1)


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['subject', 'body', 'image']

class RatingForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=1, max_value=10)

    class Meta:
        model = BookRating
        fields = ['rating']