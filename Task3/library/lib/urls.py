# lib/urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView  # Import Django's built-in LogoutView
from django.conf import settings
from django.conf.urls.static import static

app_name = "lib"

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.student_login, name='student_login'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/profile/', views.student_profile, name='student_profile'),
    
    path('logout/', views.logout_views, name='logout_views'),
    
    
    
    path('librarian/login/', views.librarian_login, name='librarian_login'),
    path('librarian/dashboard/', views.librarian_dashboard, name='librarian_dashboard'),
    path('accounts/profile/', views.custom_login_redirect, name='custom_login_redirect'),
    path('librarian/profile/', views.librarian_profile, name='librarian_profile'),
    
    path('librarian/add-book/', views.add_book, name='add_book'),
    
    path('download_template/', views.download_template, name='download_template'),
    path('upload_books/', views.upload_books, name='upload_books'),
    path('booklib/<str:isbn_number>/', views.book_detail_lib, name='book_detail_lib'),
    path('bookstu/<str:isbn_number>/', views.book_detail_stu, name='book_detail_stu'),
    
    path('borrowed_books/', views.borrowed_books, name='borrowed_books'),
    path('late_fees_details/<int:borrow_id>/', views.late_fees_details, name='late_fees_details'),
    path('issue_period/', views.issue_period, name='issue_period'),

    path('student/borrow/<str:isbn_number>/', views.borrow_book, name='borrow_book'),
    path('student/borrowed-books/', views.student_borrowed_books, name='student_borrowed_books'),
     path('return_book/<int:borrow_id>/', views.return_book, name='return_book'),
     path('feedback/', views.feedback_submission, name='student_feedback'),
     path('view_feedback/', views.view_feedback, name='view_feedback'),

     path('rate_books/', views.rate_books, name='rate_books'),
     path('librarian/ratings/', views.librarian_view_ratings, name='librarian_view_ratings'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
