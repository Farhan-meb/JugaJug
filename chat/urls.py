from django.urls import path

from chat.views import (
    ChatListView
)

app_name = 'chat'

urlpatterns = [
    path('', ChatListView.as_view(), name='chat-list'),
]
