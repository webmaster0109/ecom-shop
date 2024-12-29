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
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    gender = models.CharField(max_length=10, blank=True, choices=GENDER_CHOICES, null=True)
    dob = models.DateField(null=True, blank=True)

    verification_token = models.CharField(max_length=100, null=True, blank=True)
    verification_code = models.CharField(max_length=100, null=True, blank=True)
    is_verified = models.BooleanField(default=False, null=True, blank=True)
    forgot_password_token = models.CharField(max_length=100, null=True, blank=True)
    
    login_otp_code = models.CharField(max_length=10, null=True, blank=True)
    is_login_verify = models.BooleanField(default=False)

    is_admin = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def get_full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    def get_email(self):
        return self.user.email
    

class UserAddress(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    address = models.TextField(default='', blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.profile.user.username
    
    def get_full_address(self):
        return f'{self.address}, {self.city}, {self.state}, {self.country}, {self.zipcode}'
    
