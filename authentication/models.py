from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=50, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    gender = models.CharField(max_length=10, blank=True, choices=GENDER_CHOICES, null=True)
    dob = models.DateField(null=True, blank=True)

    verification_token = models.CharField(max_length=100, null=True, blank=True)
    verification_code = models.CharField(max_length=100, null=True, blank=True)
    is_verified = models.BooleanField(default=False, null=True, blank=True)
    forgot_password_token = models.CharField(max_length=100, null=True, blank=True)

    is_admin = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
