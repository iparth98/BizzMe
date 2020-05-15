from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import reverse
from django_countries.fields import CountryField
from PIL import Image
# Create your models here.


class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_business = models.BooleanField(default=False)


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


CATEGORY_CHOICES = (
    ('AP', "Andhra Pradesh"),
    ('MP', "Madhya Pradesh"),
    ('A', "Assam"),
    ('B', "Bihar"),
    ('CG', "Chhattisgarh"),
    ('G', "Goa"),
    ('GJ', "Gujarat"),
    ('H', "Haryana"),
)


class Business(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(default='default.jpg',
                              upload_to='profile_pics')
    business_name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=100)
    state = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.user.username}'

    def get_absolute_url(self):
        return reverse("businesses:business-info", kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default_user.jpg', upload_to='user_pictures')

    def __str__(self):
        return f'{self.user.username}'

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
