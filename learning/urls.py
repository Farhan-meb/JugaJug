from django.urls import path
from learning.views import MainPageView


app_name = 'learning'

urlpatterns = [
    path('', MainPageView.as_view(), name='learning-current'),
]
