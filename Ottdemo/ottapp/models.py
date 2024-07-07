from datetime import date, timedelta

from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


def validate_name(value):
    if not value.isalpha():
        raise ValidationError("Name should contain only alphabetical characters.")

def validate_username(value):
    if not value.isalnum():
        raise ValidationError("Username should contain only alphanumeric characters.")

def validate_dob(value):
    if value > date.today():
        raise ValidationError("Date of Birth cannot be in the future.")

    # Check if the Date of Birth is within the last 15 years
    min_age_date = date.today() - timedelta(days=15 * 365)
    if value > min_age_date:
        raise ValidationError("Date of Birth should not be within the last 15 years.")

def validate_phonenumber(value):
    if not value.isdigit() or len(value) != 10:
        raise ValidationError("Phone number should contain only 10 digits.")


class Customer(models.Model):
    firstname = models.CharField(max_length=50, validators=[validate_name])
    lastname = models.CharField(max_length=50, validators=[validate_name])
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True, validators=[validate_username])
    password = models.CharField(max_length=100)  # You should use a more secure way to store passwords
    DoB = models.DateField(validators=[validate_dob])
    phonenumber = models.CharField(max_length=15, validators=[validate_phonenumber])





class UserProfile(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='profile_images/')
    pin = models.CharField(max_length=6, null=True, blank=True)  # Hashed PIN

    def set_pin(self, raw_pin):
        self.pin = make_password(raw_pin)

    def check_pin(self, raw_pin):
        return check_password(raw_pin, self.pin) if self.pin else False

    def __str__(self):
        return self.name


class KidsProfile(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='profile_images/')

MOVIE_CHOICES = (
    ('seasonal', 'Seasonal'),
    ('single', 'Single')
)

GENRE_CHOICES = [
    ('action', 'Action'),
    ('comedy', 'Comedy'),
    ('drama', 'Drama'),
    ('horror', 'Horror'),
    ('romance', 'Romance'),
    ('science_fiction', 'Science Fiction'),
    ('fantasy', 'Fantasy'),
]
LANGUAGE_CHOICES = [
    ('english', 'English'),
    ('hindi', 'Hindi'),
    ('malayalam', 'Malayalam'),
    ('tamil', 'Tamil'),
    ('kannada', 'Kannada'),
    ('telugu', 'Telugu'),
    ('bengali', 'Bengali'),
]

class Adult_Movie(models.Model):
    title = models.CharField(max_length=255)
    description=models.TextField(max_length=500,default='')
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES)
    release_date = models.DateField()
    language = models.CharField(max_length=100, choices=LANGUAGE_CHOICES)
    actor = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    ratings = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    image = models.ImageField(upload_to='movie_image/')
    image_cover = models.ImageField(upload_to='movie_images/')
    video = models.FileField(upload_to='movie_videos/')
    def _str_(self):
        return self.title


class Kids_Movie(models.Model):
    title = models.CharField(max_length=255)
    description=models.TextField(max_length=500,default='')
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES)
    release_date = models.DateField()
    language = models.CharField(max_length=100, choices=LANGUAGE_CHOICES)
    actor = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    ratings = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    image = models.ImageField(upload_to='movie_image/')
    image_cover = models.ImageField(upload_to='movie_images/')
    video = models.FileField(upload_to='movie_videos/')

    def _str_(self):
        return self.title

class Adult_WatchHistory(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Adult_Movie, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Adult_WatchLater(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Adult_Movie, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

class Adult_Suggestions(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    suggested_movie = models.ForeignKey(Adult_Movie, on_delete=models.CASCADE)

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    duration_months = models.IntegerField()
    # Add more details as needed

class UserSubscription(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    # Add more details as needed
