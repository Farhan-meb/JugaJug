from django.urls import path
from learning.views import (MainPageView,
                            ProblemListView,
                            ProblemDetailView)


app_name = 'learning'

urlpatterns = [
    path('', MainPageView.as_view(), name='learning-current'),
    path('problems/', ProblemListView.as_view(), name='problem-list'),
    path('problems/<int:pk>/', ProblemDetailView.as_view(), name='problem-details'),
]
