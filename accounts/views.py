import sys

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from accounts.models import Profile
from django.views.generic import (
    ListView,
)
from django.shortcuts import render, get_object_or_404
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from accounts.models import Profile,Follow
from blog.models import Post
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


class UserListView(LoginRequiredMixin,ListView):
    model = Profile
    template_name = 'accounts/user_list.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            return Profile.objects.filter(user__username__contains=query)
        return Profile.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = False
        if self.request.GET.get('query'):
            context['search'] = True
        context.update({
            'dashboard_users_tab': 'active'
        })
        return context


class FollowsListView(LoginRequiredMixin,ListView):
    model = Follow
    template_name = 'accounts/follow.html'
    context_object_name = 'follows'

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_queryset(self):
        user = self.visible_user()
        return Follow.objects.filter(user=user).order_by('-date')

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['follow'] = 'follows'
        return data


class FollowersListView(LoginRequiredMixin,ListView):
    model = Follow
    template_name = 'accounts/follow.html'
    context_object_name = 'follows'

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_queryset(self):
        user = self.visible_user()
        return Follow.objects.filter(follow_user=user).order_by('-date')

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['follow'] = 'followers'
        data['profile'] = Profile.objects.get(Q(user__username=self.kwargs.get('username'))),
        return data


class UserProfileView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'accounts/user_profile_details.html'
    context_object_name = 'blogs'
    paginate_by = 3

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_context_data(self, **kwargs):
        visible_user = self.visible_user()
        logged_user = self.request.user

        if logged_user.username == '' or logged_user is None:
            can_follow = False
        else:
            can_follow = (Follow.objects.filter(user=logged_user,
                                                follow_user=visible_user).count() == 0)
        data = super().get_context_data(**kwargs)

        data['user_profile'] = visible_user
        data['can_follow'] = can_follow
        data.update({
            'blog_nav': 'active',
            'profile': Profile.objects.get(Q(user__username=self.kwargs.get('username'))),

        })
        return data

    def get_queryset(self):
        user = self.visible_user()
        return Post.objects.filter(author=user).order_by('-created_at')

    def post(self, request, *args, **kwargs):
        if request.user.id is not None:
            follows_between = Follow.objects.filter(user=request.user,
                                                    follow_user=self.visible_user())

            if 'follow' in request.POST:
                    new_relation = Follow(user=request.user, follow_user=self.visible_user())
                    if follows_between.count() == 0:
                        new_relation.save()
            elif 'unfollow' in request.POST:
                    if follows_between.count() > 0:
                        follows_between.delete()

        return self.get(self, request, *args, **kwargs)


class CurrentUserProfileView(LoginRequiredMixin,ListView):
    model = Post
    paginate_by = 2
    context_object_name = 'blogs'
    template_name = 'accounts/user_profile_details_current.html'

    def get_queryset(self):
        return Post.objects.filter(Q(author__username=self.kwargs.get('username')))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'blog_nav': 'active',
            'profile': Profile.objects.get(Q(user__username=self.kwargs.get('username'))),
            'dashboard_profile_tab': 'active'

        })
        return context