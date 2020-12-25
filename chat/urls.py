from django.urls import path

from chat.views import (
    ChatListView,
    ChatDetailsView
)

app_name = 'chat'

urlpatterns = [
    path('', ChatListView.as_view(), name='chat-list'),
    path('<int:reciever_id>/', ChatDetailsView.as_view(), name='chat-details'),
]
