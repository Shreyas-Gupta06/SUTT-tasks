from django.urls import path
from . import views

app_name = "lib"

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.student_login, name='student_login'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/profile/', views.student_profile, name='student_profile'),
    path('logout/google/', views.google_logout, name='google_logout'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('librarian/login/', views.librarian_login, name='librarian_login'),
    path('librarian/dashboard/', views.librarian_dashboard, name='librarian_dashboard'),
    path('accounts/profile/', views.custom_login_redirect, name='custom_login_redirect'),
]
