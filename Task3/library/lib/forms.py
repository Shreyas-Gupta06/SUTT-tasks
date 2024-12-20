# lib/forms.py
from django import forms
from .models import StudentProfile
from .models import LibrarianProfile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['room_number', 'hostel']

class LibrarianProfileForm(forms.ModelForm):
    class Meta:
        model = LibrarianProfile
        fields = ['psrn_number', 'name']
