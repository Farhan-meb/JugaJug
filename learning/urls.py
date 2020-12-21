from django.urls import path
from learning.views import (MainPageView,
                            ProblemListView,
                            ProblemDetailView,
                            SubmissionCreateView,
                            SubmissionListView)


app_name = 'learning'

urlpatterns = [
    path('', MainPageView.as_view(), name='learning-current'),
    path('problems/', ProblemListView.as_view(), name='problem-list'),
    path('problems/<int:pk>/', ProblemDetailView.as_view(), name='problem-details'),
    path('problems/<int:problem_id>/submit/', SubmissionCreateView.as_view(), name='submission-create'),
    path('submissions/', SubmissionListView.as_view(), name='submission-list'),
]
