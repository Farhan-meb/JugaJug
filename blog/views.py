from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
import sys
from django.db.models import Count
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DeleteView,
    CreateView,
    UpdateView,
    DetailView
)
from accounts.models import Profile,Follow
from blog.forms import BlogForm,NewCommentForm
from blog.models import Post,Comments,Preference
from django.contrib.auth.decorators import login_required


class BlogListView(ListView):
    model = Post
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'
    ordering = ['-created_at']
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_users = []
        data_counter = Post.objects.values('author')\
            .annotate(author_count=Count('author'))\
            .order_by('-author_count')[:6]

        for aux in data_counter:
            all_users.append(User.objects.filter(pk=aux['author']).first())

        context['preference'] = Preference.objects.all()
        context['all_users'] = all_users
        print(all_users, file=sys.stderr)
        context.update({
            'blog_nav': 'active',
            'dashboard_home_tab': 'active'
        })
        return context


    def get_queryset(self):
        user = self.request.user
        qs = Follow.objects.filter(user=user)
        follows = [user]
        for obj in qs:
            follows.append(obj.follow_user)
        return Post.objects.filter(author__in=follows).order_by('-created_at')


class UserProfileView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/user_profile_details.html'
    context_object_name = 'blogs'
    paginate_by = 3

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_context_data(self, **kwargs):
        visible_user = self.visible_user()
        logged_user = self.request.user
        print(logged_user.username == '', file=sys.stderr)

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


class CurrentUserProfileView(ListView):
    model = Post
    paginate_by = 2
    context_object_name = 'blogs'
    template_name = 'blog/user_profile_details_current.html'

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


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/blog_form.html'
    form_class = BlogForm
    success_url = reverse_lazy('blog-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'blog_nav': 'active',
            'card_header': 'New Post',
            'operation': 'Create'
        })
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        #print(form.instance.user)
        return super().form_valid(form)


class BlogUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/blog_form.html'
    context_object_name = 'blog'
    form_class = BlogForm
    success_url = reverse_lazy('blog-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'blog_nav': 'active',
            'card_header': 'Update Blog',
            'operation': 'Update'
        })
        return context

    def test_func(self):
        return self.request.user == self.get_object().author


class BlogDeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/blog_delete.html'
    success_url = reverse_lazy('blog-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'blog_nav': 'active'
        })
        return context

    def test_func(self):
        return self.request.user == self.get_object().author


class BlogDetailView(DetailView):
    model = Post
    template_name = 'blog/blog_details.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments_connected = Comments.objects.filter(post_connected=self.get_object()).order_by('-date_posted')
        context.update({
            'blog_nav': 'active',
            'comments': comments_connected,
            'form': NewCommentForm(instance=self.request.user),
        })
        return context

    def post(self, request, *args, **kwargs):
        new_comment = Comments(Comment=request.POST.get('Comment'),
                              author=self.request.user,
                              post_connected=self.get_object(),)
        new_comment.save()
#
        return self.get(self, request, *args, **kwargs)


class FollowsListView(ListView):
    model = Follow
    template_name = 'blog/follow.html'
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


class FollowersListView(ListView):
    model = Follow
    template_name = 'blog/follow.html'
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


