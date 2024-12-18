from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from .forms import ProfileForm
from .models import StudentProfile


def librarian_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('lib:librarian_dashboard')  # Redirect to the librarian dashboard after login
    else:
        form = AuthenticationForm()
    return render(request, 'lib/librarian_login.html', {'form': form})

def home(request):
    return render(request, 'lib/base.html')


def student_login(request):
    return render(request, 'lib/student_login.html')

@login_required(login_url='/login/')
def student_dashboard(request):
    return render(request, 'lib/student_dashboard.html')

@login_required(login_url='/librarian/login/')
def librarian_dashboard(request):
    return render(request, 'lib/librarian_dashboard.html')


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

def google_logout(request):
    # First log the user out from Django
    logout(request)
    
    # Now, redirect to Google logout URL to ensure the user is logged out of Google
    return redirect('https://accounts.google.com/Logout')

def google_login_callback(request):
    user = request.user  # The user is already logged in after Google OAuth
    print(f"Logged in user: {user.username}")  # Check if this prints the logged-in user
    if not hasattr(user, 'studentprofile'):
        print("Creating student profile")
        StudentProfile.objects.create(user=user)
    return redirect('lib:student_dashboard')
