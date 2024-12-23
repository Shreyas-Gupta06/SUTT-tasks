from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import ProfileForm
from .models import StudentProfile
from .models import LibrarianProfile, Book, Borrow, GlobalSettings
from .forms import LibrarianProfileForm, IssuePeriodForm, GlobalSettings
from .forms import BookForm  # Ensure you have a BookForm for creating books
from django.http import HttpResponse
import os
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, timedelta

from django.contrib.admin.views.decorators import staff_member_required

from .forms import BookForm

import pandas as pd
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .forms import LateFeesForm 
from .models import Borrow, GlobalSettings
from datetime import timedelta
from django.utils import timezone



@staff_member_required
def borrowed_books(request):
    borrowed_books = Borrow.objects.select_related('book', 'student').all()
    return render(request, 'lib/borrowed_books.html', {'borrowed_books': borrowed_books})



@staff_member_required
def late_fees_details(request, borrow_id):
    borrow = get_object_or_404(Borrow, id=borrow_id)
    if request.method == 'POST':
        form = LateFeesForm(request.POST)
        if form.is_valid():
            late_fees = form.cleaned_data['late_fees']
            # Assuming Borrow model has a field for late_fees
            borrow.late_fees = late_fees
            borrow.save()
            return redirect('lib:borrowed_books')
    else:
        form = LateFeesForm()
    return render(request, 'lib/late_fees_details.html', {'form': form, 'borrow': borrow})

@staff_member_required
def issue_period(request):
    global_settings = GlobalSettings.objects.first()
    current_issue_period = global_settings.issue_period if global_settings else 'Not Set'

    if request.method == 'POST':
        form = IssuePeriodForm(request.POST)
        if form.is_valid():
            issue_period = form.cleaned_data['issue_period']
            if global_settings:
                global_settings.issue_period = issue_period
                global_settings.save()
            else:
                GlobalSettings.objects.create(issue_period=issue_period)
            return redirect('lib:issue_period')
    else:
        form = IssuePeriodForm()

    return render(request, 'lib/issue_period.html', {
        'form': form,
        'current_issue_period': current_issue_period
    })

@staff_member_required
def download_template(request):
    file_path = os.path.join(settings.BASE_DIR, 'lib', 'static', 'excel', 'book_template.xlsx')
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='book_template.xlsx')
    else:
        return HttpResponse("File not found.")
    
@staff_member_required
def book_detail_lib(request, isbn_number):
    book = get_object_or_404(Book, isbn_number=isbn_number)
    if request.method == 'POST':

        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('lib:librarian_dashboard')
        else:
            print("Form is not valid:", form.errors)
    else:
        form = BookForm(instance=book)

    return render(request, 'lib/book_detail_lib.html', {'form': form, 'book': book})


@login_required(login_url='/login/')
def book_detail_stu(request, isbn_number):
    book = get_object_or_404(Book, isbn_number=isbn_number)
    return render(request, 'lib/book_detail_stu.html', {'book': book})



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
        form = BookForm(request.POST, request.FILES)  # Include request.FILES for handling file uploads
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            return redirect('lib:librarian_dashboard')  # Redirect to librarian_dashboard after successful addition
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
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()

    return render(request, 'lib/librarian_dashboard.html', {'books': books})





@login_required(login_url='/login/')
def student_dashboard(request):
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()
    
    return render(request, 'lib/student_dashboard.html', {'books': books})

@login_required(login_url='/login/')
def borrow_book(request, isbn_number):
    book = get_object_or_404(Book, isbn_number=isbn_number)
    student_profile = get_object_or_404(StudentProfile, user=request.user)
    global_settings = GlobalSettings.objects.first()
    if book.available_copies > 0:
        book.available_copies -= 1
        book.save()
        
        borrow = Borrow(student=student_profile, book=book, issued_date=datetime.now())
        borrow.due_date = borrow.issued_date + timedelta(days = global_settings.issue_period)
        borrow.save()
        return redirect('lib:student_dashboard')
    else:
        return render(request, 'lib/student_dashboard.html', {'books': Book.objects.all(), 'error': 'Book not available'})









@login_required(login_url='/login/')
def student_borrowed_books(request):
    student_profile = get_object_or_404(StudentProfile, user=request.user)
    borrowed_books = Borrow.objects.filter(student=student_profile)
    
    # srijan is gay (hidden line, sutta if u see this brownie points for u)

    return render(request, 'lib/student_borrowed_books.html', {'borrowed_books': borrowed_books})





@login_required(login_url='/login/')
def return_book(request, borrow_id):
    borrow = get_object_or_404(Borrow, id=borrow_id)
    book = borrow.book

    # Increment the available copies
    book.available_copies += 1
    book.save()

    # Delete the borrow record
    borrow.delete()

    return redirect('lib:student_borrowed_books')