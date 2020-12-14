from django.urls import path
from accounts import views as user_views

app_name = 'accounts'

urlpatterns = [
    path('update-profile/', user_views.profile, name='update-profile'),
]
