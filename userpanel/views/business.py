from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DetailView
from ..forms import BusinessSignUpForm, UserUpdateForm, ProfileUpdateForm
from ..models import User, Business


class BusinessSignUpView(CreateView):
    model = User
    form_class = BusinessSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'business'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')
# ye kaha se aya?muje kya pata

@login_required
def business_home(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect("businesses:business-dashboard")

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'business/business_dashboard.html', context)


class BusinessCreateView(LoginRequiredMixin, CreateView):
    model = Business
    fields = ['business_name', 'description',
              'address', 'state', 'country', 'zip', 'image']
    template_name = 'business/business_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BusinessDetailView(DetailView):
    model = Business
    template_name = 'business/business_info.html'
