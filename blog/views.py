import self as self
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
    DetailView,
    TemplateView
)
from accounts.models import Profile,Follow
from blog.forms import BlogForm,NewCommentForm
from blog.models import Post,Comments,Preference
from django.contrib.auth.decorators import login_required


class BlogListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'
    ordering = ['-created_at']
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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


class BlogDetailView(LoginRequiredMixin,DetailView):
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


class SerchaPostView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blog/search_post.html'
    context_object_name = 'blogs'
    ordering = ['-created_at']

    paginate_by = 3

    def get_queryset(self):
        user = self.request.user
        qs = Follow.objects.filter(user=user)
        follows = [user]
        for obj in qs:
            follows.append(obj.follow_user)
        query = self.request.GET.get('query')
        return Post.objects.filter(title__contains = query,content__contains=query,author__in=follows).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'blog_nav': 'active',
            'dashboard_home_tab': 'active'
        })
        return context

@login_required
def postpreference(request, postid, userpreference):
    if request.method == "POST":
        eachpost = get_object_or_404(Post, id=postid)
        obj = ''
        valueobj = ''
        print(request.POST.get('post_id'))
        print(postid)
        try:
            obj = Preference.objects.get(user=request.user, post=eachpost)
            valueobj = obj.value  # value of userpreference
            valueobj = int(valueobj)
            userpreference = int(userpreference)

            if valueobj != userpreference:
                obj.delete()

                upref = Preference()
                upref.user = request.user

                upref.post = eachpost

                upref.value = userpreference

                if userpreference == 1 and valueobj != 1:
                    eachpost.likes += 1
                    eachpost.dislikes -= 1
                elif userpreference == 2 and valueobj != 2:
                    eachpost.dislikes += 1
                    eachpost.likes -= 1

                upref.save()

                eachpost.save()

                context = {'eachpost': eachpost,
                           'postid': postid}

                return redirect(reverse_lazy('blog:blog-details', kwargs={"pk": postid}))

            elif valueobj == userpreference:
                obj.delete()

                if userpreference == 1:
                    eachpost.likes -= 1
                elif userpreference == 2:
                    eachpost.dislikes -= 1

                eachpost.save()

                context = {'eachpost': eachpost,
                           'postid': postid}

                return redirect(reverse_lazy('blog:blog-details', kwargs={"pk": postid}))

        except Preference.DoesNotExist:
            upref = Preference()

            upref.user = request.user

            upref.post = eachpost

            upref.value = userpreference

            userpreference = int(userpreference)

            if userpreference == 1:
                eachpost.likes += 1
            elif userpreference == 2:
                eachpost.dislikes += 1

            upref.save()

            eachpost.save()

            context = {'eachpost': eachpost,
                       'postid': postid}

            return redirect(reverse_lazy('blog:blog-details', kwargs={"pk": postid}))

    else:
        eachpost = get_object_or_404(Post, id=postid)
        context = {'eachpost': eachpost,
                   'postid': postid}

        return redirect(reverse_lazy('blog:blog-details', kwargs={"pk": postid}))