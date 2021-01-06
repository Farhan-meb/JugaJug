from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from chat.models import Messages
from accounts.models import Follow
from chat.forms import NewMessageForm


class ChatListView(LoginRequiredMixin,ListView):
    model = Follow
    template_name = 'chat/message_list.html'
    context_object_name = 'follows'

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(user=user).order_by('-date')

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['follow'] = 'follows'
        user_ids = [user.follow_user.id for user in self.get_queryset()]
        #print(user_ids)
        user_ids.extend([user.id for user in Follow.objects.filter(follow_user=self.request.user)])
        #print(user_ids)
        user_ids = set(user_ids)
        #print(self.request.user.id)
        data['users'] = User.objects.filter(id__in = user_ids)
        data.update({
            'dashboard_chat_tab':'active'
        })
        return data


class ChatDetailsView(LoginRequiredMixin,ListView):
    model = Messages
    template_name = 'chat/chat_details.html'
    context_object_name = 'chats'

    def get_queryset(self):
        user = self.request.user
        chats = Messages.objects.filter\
            (Q(sender = user, reciever__id = self.kwargs.get('reciever_id')) |
             Q(reciever = user, sender__id = self.kwargs.get('reciever_id')))\
            .order_by('-created_at')
        return chats

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'dashboard_chat_tab': 'active',
            'form': NewMessageForm,
        })
        return context

    def post(self, request, *args, **kwargs):
        new_message = Messages(message=request.POST.get('message'),
                               sender=self.request.user,
                               reciever_id = self.kwargs.get('reciever_id'),)
        new_message.save()
        return self.get(self, request, *args, **kwargs)