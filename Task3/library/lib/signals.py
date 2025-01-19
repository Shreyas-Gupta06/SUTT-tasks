from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LibrarianProfile, StudentProfile
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Attempt to get or create the LibrarianProfile and handle its creation if it doesn't exist
        # if not hasattr(instance, 'librarianprofile') and not hasattr(instance, 'studentprofile'): check 
            librarian_profile, librarian_created = LibrarianProfile.objects.get_or_create(user=instance)
            if librarian_created:
                # If the librarian profile was created, ensure no student profile exists
                StudentProfile.objects.filter(user=instance).delete()
            else:
                # If the librarian profile already existed, create a student profile
                StudentProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Save the LibrarianProfile if it exists
    if LibrarianProfile.objects.filter(user=instance).exists():
        instance.librarianprofile.save()
    # Save the StudentProfile if it exists
    elif StudentProfile.objects.filter(user=instance).exists():
        instance.studentprofile.save()

