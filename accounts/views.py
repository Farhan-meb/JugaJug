from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from accounts.models import Profile
from django.views.generic import (
    ListView,
)
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


User = get_user_model()


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


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
            return redirect('accounts:update-profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    context.update({
        'dashboard_settings_tab': 'active'
    })

    return render(request, 'accounts/profile_update.html', context)


class UserListView(ListView):
    model = Profile
    template_name = 'accounts/user_list.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        return Profile.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'dashboard_users_tab': 'active'
        })
        return context