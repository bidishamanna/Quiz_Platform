from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Role constants
    STAFF = 'staff'
    STUDENT = 'student'

    ROLE_CHOICES = [
        (STAFF, 'Staff'),
        (STUDENT, 'Student'),
    ]

    # Override AbstractUser fields
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)  # Required by AbstractUser
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    # Custom fields
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    gender = models.CharField(max_length=10, choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ])
    dob = models.DateField()

    # Use email to log in
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name','gender','dob']

    def __str__(self):
        return f"{self.email} ({self.role})"


class UserToken(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='tokens')
    tokens = models.CharField(max_length=250,unique=True)    
    created_at = models.DateField(auto_now_add=True)
    expired_at = models.DateField()

    def __str__(self):
        return f"Token for {self.user.email}(Expires:{self.expired_at})"
    

