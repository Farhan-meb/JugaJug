from django.db.models import Count,Q
from django.shortcuts import render
from learning.models import (
    Problem,
    Tutorial,
    Score,
    Submission
)
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import (
    DetailView,
    ListView,
    CreateView
)
from learning.forms import SubmissionForm


class MainPageView(ListView):

    template_name = 'learning/main_page.html'

    def get_queryset(self):
        return Problem.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'blog_nav': 'active',
            'tutorials': Tutorial.objects.all(),
            'current_user': Score.objects.filter(learner=self.request.user),
            'dashboard_learning_tab': 'active',
            'dashboard_Tuto_tab': 'active'
        })
        return context


class ProblemListView(ListView):
    model = Problem
    context_object_name = 'problems'
    template_name = 'learning/problems_list.html'

    def get_queryset(self):
        """
        Returns a queryset containing problems in descending order based on the number
        of people who solved each problem
        - It uses annotation and aggregation to calculate the problem solution count
        by number of unique users for each problem
        """

        current_user = self.request.user if self.request.user.is_authenticated else None
        return Problem.objects.annotate(
            solve_count=Count(
                'submissions__user',
                filter=Q(submissions__status='AC'),
                distinct=True
            ),
            is_solved=Count(
                'submissions__user',
                filter=Q(submissions__status='AC', submissions__user=current_user)
            )
        ).order_by('-solve_count')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'dashboard_learning_tab': 'active',
            'dashboard_Prob_tab': 'active',
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
            'dashboard_Prob_tab': 'active',
            'submission_form': SubmissionForm(),
            'testcases': self.get_object().testcases.filter(is_sample=True)
        })
        return context


class SubmissionCreateView(CreateView):
    model = Submission
    form_class = SubmissionForm
    success_url = reverse_lazy('learning:submission-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.problem = get_object_or_404(Problem, pk=self.kwargs.get('problem_id'))
        return super().form_valid(form)


class SubmissionListView(ListView):
    model = Submission
    paginate_by = 10
    context_object_name = 'submissions'
    template_name = 'learning/submission_list.html'

    def get_queryset(self):
        return Submission.objects.filter(user = self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'dashboard_learning_tab': 'active',
            'dashboard_Sub_tab': 'active'
        })
        return context