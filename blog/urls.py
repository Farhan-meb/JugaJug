from django.urls import path

from blog.views import (
    BlogListView,
    BlogCreateView,
    BlogUpdateView,
    BlogDetailView,
    BlogDeleteView,
    postpreference
)

app_name = 'blog'

urlpatterns = [
    path('new/', BlogCreateView.as_view(), name='blog-create'),
    path('<int:pk>/update/', BlogUpdateView.as_view(), name='blog-update'),
    path('<int:pk>/delete/', BlogDeleteView.as_view(), name='blog-delete'),
    path('<int:pk>/', BlogDetailView.as_view(), name='blog-details'),
    path('post/<int:postid>/preference/<int:userpreference>/', postpreference, name='postpreference'),
]
