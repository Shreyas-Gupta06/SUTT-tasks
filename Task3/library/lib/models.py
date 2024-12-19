# lib/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=20, blank=True, null=True)
    hostel = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username

# Automatically create a StudentProfile when a new User is created
@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created:  # When a new User is created
        StudentProfile.objects.create(user=instance)

# Automatically save the StudentProfile when the User is saved
@receiver(post_save, sender=User)
def save_student_profile(sender, instance, **kwargs):
    instance.studentprofile.save()

