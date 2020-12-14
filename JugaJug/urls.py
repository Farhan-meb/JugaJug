
from django.contrib import admin
from django.urls import path,include
from blog.views import BlogListView,UserProfileView,CurrentUserProfileView,FollowsListView,FollowersListView
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from accounts import views as account_views
from accounts.views import UserListView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    #blog urls
    path('', BlogListView.as_view(), name='blog-list'),

    #app urls
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('accounts/', include('accounts.urls')),

    #profile
    path('User/<str:username>/', UserProfileView.as_view(), name='user-profile'),
    path('User/<str:username>/Profile', CurrentUserProfileView.as_view(), name='user-profile-current'),
    path('Users/', UserListView.as_view(), name='user-list'),

    path('<str:username>/follows', FollowsListView.as_view(), name='user-follows'),
    path('<str:username>/followers', FollowersListView.as_view(), name='user-followers'),

    #auth urls
    path('register/', account_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)