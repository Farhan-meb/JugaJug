from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from chat.models import Messages
from django.db.models import Q
from accounts.models import Follow, Profile


class ChatListView(ListView):
    model = Follow
    template_name = 'chat/message_list.html'
    context_object_name = 'follows'

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(Q(user=user)|Q(follow_user=user)).order_by('-date')

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['follow'] = 'follows'
        return data
