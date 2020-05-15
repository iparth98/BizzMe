from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer, Profile, User


class CustomerSignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True
        if commit:
            user.save()
            customer = Customer.objects.create(user=user)
            profile = Profile.objects.create(user=user)
        return user

    def __init__(self, *args, **kwargs):
        super(CustomerSignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['email', 'password1']:
            self.fields[fieldname].help_text = None


class BusinessSignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_business = True
        if commit:
            user.save()
            profile_b = Profile.objects.create(user=user)
        return user

    def __init__(self, *args, **kwargs):
        super(BusinessSignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['email', 'password1']:
            self.fields[fieldname].help_text = None


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
