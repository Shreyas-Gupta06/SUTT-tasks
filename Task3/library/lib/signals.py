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