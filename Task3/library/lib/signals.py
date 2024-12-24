from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import StudentProfile, LibrarianProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff:
            LibrarianProfile.objects.get_or_create(user=instance)
        else:
            StudentProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_staff:
        if hasattr(instance, 'librarianprofile'):
            instance.librarianprofile.save()
    else:
        if hasattr(instance, 'studentprofile'):
            instance.studentprofile.save()



# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import LibrarianProfile, StudentProfile
# from django.contrib.auth.models import User

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         # Create the librarian profile
#         if instance.librarianprofile:
#             LibrarianProfile.objects.get_or_create(user=instance)
            
#             # Check if the student profile exists with the same user name and delete it
#             try:
#                 student_profile = StudentProfile.objects.get(user=instance)
#                 student_profile.delete()
#             except StudentProfile.DoesNotExist:
#                 pass  # No student profile to delete, so pass

#         # Create a student profile only if the user isn't a librarian
#         else:
#             StudentProfile.objects.get_or_create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     if hasattr(instance, 'librarianprofile'):
#         instance.librarianprofile.save()
#     else:
#         if hasattr(instance, 'studentprofile'):
#             instance.studentprofile.save()
