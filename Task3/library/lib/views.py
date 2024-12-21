from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import ProfileForm
from .models import StudentProfile
from .models import LibrarianProfile, Book
from .forms import LibrarianProfileForm
from .forms import BookForm  # Ensure you have a BookForm for creating books
from django.http import HttpResponse
import os
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect


from django.contrib.admin.views.decorators import staff_member_required

from .forms import BookForm

import pandas as pd

from django.contrib.admin.views.decorators import staff_member_required
from django.http import FileResponse

@staff_member_required
def download_template(request):
    file_path = os.path.join(settings.BASE_DIR, 'lib', 'static', 'excel', 'book_template.xlsx')
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='book_template.xlsx')
    else:
        return HttpResponse("File not found.")



@staff_member_required
def upload_books(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']
        try:
            df = pd.read_excel(excel_file)
            df.columns = df.columns.str.strip()  # Remove any leading/trailing whitespace from columns
            
            # Ensure the dates are correctly parsed
            df['Published Date'] = pd.to_datetime(df['Published Date'], format='%d-%m-%Y', errors='coerce')
            
            for _, row in df.iterrows():
                Book.objects.create(
                    title=row['Title'],
                    author=row['Author'],
                    genre=row['Genre'],
                    published_date=row['Published Date'],
                    isbn_number=row['ISBN Number'],
                    available_copies=row['Available Copies']
                )
            messages.success(request, "Books uploaded successfully!")
        except Exception as e:
            messages.error(request, f"Error uploading books: {str(e)}")
        return redirect('lib:librarian_dashboard')
    return render(request, 'lib/addbook.html')


@staff_member_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new book
            messages.success(request, 'Book added successfully!')  # Show success message
            return redirect('lib:librarian_dashboard')  # Redirect to dashboard after success
    else:
        form = BookForm()

    return render(request, 'lib/addbook.html', {'form': form})



@staff_member_required
def librarian_profile(request):
    profile, created = LibrarianProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = LibrarianProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('lib:librarian_profile')
    else:
        form = LibrarianProfileForm(instance=profile)

    return render(request, 'lib/librarian_profile.html', {'form': form})    

def home(request):
    return render(request, 'lib/base.html')


def student_login(request):
    return render(request, 'lib/student_login.html')

@login_required(login_url='/login/')
def student_dashboard(request):
    return render(request, 'lib/student_dashboard.html')




@login_required(login_url='/login/')
def student_profile(request):
    # Check if a profile exists for the user, or create a new one
    user_profile, created = StudentProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()  # Save the updated profile
            return redirect('lib:student_profile')  # Redirect to profile page
    else:
        form = ProfileForm(instance=user_profile)  # Pre-fill form with current profile data

    return render(request, 'lib/student_profile.html', {'form': form})

@login_required
def custom_login_redirect(request):
    if request.user.is_staff:
        # Redirect to librarian dashboard
        return redirect('lib:librarian_dashboard')
    else:
        # Redirect to student dashboard
        return redirect('lib:student_dashboard')

def logout_views(request):
    # First log the user out from Django
    logout(request)
    
    # Now, redirect to Google logout URL to ensure the user is logged out of Google
    return redirect('lib:home')


@staff_member_required
def librarian_profile(request):
    profile, created = LibrarianProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = LibrarianProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('lib:librarian_profile')
    else:
        form = LibrarianProfileForm(instance=profile)

    return render(request, 'lib/librarian_profile.html', {'form': form})

def librarian_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect to librarian dashboard after login
            return redirect('lib:librarian_dashboard') 
    else:
        form = AuthenticationForm()

    return render(request, 'lib/librarian_login.html', {'form': form})


@staff_member_required
def librarian_dashboard(request):
    # Fetching all books for the librarian to view
    books = Book.objects.all()
    
    return render(request, 'lib/librarian_dashboard.html', {'books': books})