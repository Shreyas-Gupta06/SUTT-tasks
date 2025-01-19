from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.core.exceptions import ImmediateHttpResponse
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email_domain = sociallogin.account.extra_data['email'].split('@')[1]
        allowed_domain = 'pilani.bits-pilani.ac.in'
        if email_domain != allowed_domain:
            # Add a message to the request
            messages.error(request, f"Email domain must be {allowed_domain}")
            # Redirect to the login page
            raise ImmediateHttpResponse(redirect('lib:student_login'))

