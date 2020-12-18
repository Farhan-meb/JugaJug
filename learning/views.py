from django.shortcuts import render
from learning.models import Problem, Tutorial, Score
from django.views.generic import (
    DetailView,
    ListView
)


class MainPageView(ListView):
    model = Problem
    context_object_name = 'problems'
    template_name = 'learning/main_page.html'

    def get_queryset(self):
        return Problem.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'blog_nav': 'active',
            'tutorials': Tutorial.objects.all(),
            'score': Score.objects.filter(learner=self.request.user),
            'dashboard_learning_tab': 'active'
        })
        return context
