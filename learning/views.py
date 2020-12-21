from django.shortcuts import render
from learning.models import Problem, Tutorial, Score
from django.contrib.auth.models import User
from django.views.generic import (
    DetailView,
    ListView
)
from learning.forms import SubmissionForm

class MainPageView(ListView):

    template_name = 'learning/main_page.html'
    Score.learner = User

    def get_queryset(self):
        return Problem.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'blog_nav': 'active',
            'tutorials': Tutorial.objects.all(),
            'current_user': Score.objects.filter(learner=self.request.user),
            'dashboard_learning_tab': 'active'
        })
        return context


class ProblemListView(ListView):
    model = Problem
    context_object_name = 'problems'
    template_name = 'learning/problems_list.html'

    def get_queryset(self):
        return Problem.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'dashboard_learning_tab': 'active',
            'current_user': Score.objects.filter(learner=self.request.user)
        })
        return context


class ProblemDetailView(DetailView):
    model = Problem
    template_name = 'learning/problem_details.html'
    context_object_name = 'problem'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'dashboard_learning_tab': 'active',
            'submission_form': SubmissionForm(),
        })
        return context