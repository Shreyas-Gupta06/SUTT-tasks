from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import StudentProfile, LibrarianProfile, Book, Borrow, GlobalSettings, Feedback

# Define an inline admin descriptor for StudentProfile model
class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    verbose_name_plural = 'student profiles'

# Define an inline admin descriptor for LibrarianProfile model
class LibrarianProfileInline(admin.StackedInline):
    model = LibrarianProfile
    can_delete = False
    verbose_name_plural = 'librarian profiles'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (StudentProfileInline, LibrarianProfileInline)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)



# Register your models here.

admin.site.register(StudentProfile)
admin.site.register(LibrarianProfile)
admin.site.register(Book)
admin.site.register(Borrow)
admin.site.register(GlobalSettings)
admin.site.register(Feedback)
