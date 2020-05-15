from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from ecommerce.models import Item
from django.contrib.auth.decorators import login_required
from userpanel.forms import UserUpdateForm, ProfileUpdateForm


class HomeView(ListView):
    model = Item
    paginate_by = 6 
    context_object_name = 'items'
    template_name = 'home.html'


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def loginfunc(request):
    return render(request, 'registration/login.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact-page.html')


def accountvalidation(request):
    if request.user.is_authenticated:
        if request.user.is_business:
            return redirect('businesses:business-dashboard')
        else:
            return redirect('home')
    return render(request, 'home.html')


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'account/profile.html', context)
