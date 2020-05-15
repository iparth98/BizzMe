from django.contrib import admin
from .models import User, Customer, Business, Profile

# Register your models here.

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Business)
admin.site.register(Profile)
