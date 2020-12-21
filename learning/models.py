from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from learning.utils import submission_directory_path


class Tutorial(models.Model):
    title = models.CharField(max_length=50, blank=True)
    content = RichTextField()
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    problem_ids = models.JSONField(verbose_name="Problem Id's", default=list)


class Score(models.Model):
    learner = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    solved = models.IntegerField(default=0)


class Problem(models.Model):
    name = models.CharField(max_length=100)
    score = models.IntegerField(default=-1)
    statement = models.TextField()
    input_section = models.TextField()
    output_section = models.TextField()
    time_limit = models.IntegerField(verbose_name='Time Limit', default=1)
    memory_limit = models.PositiveIntegerField(verbose_name='Memory Limit', default=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Submission(models.Model):
    STATUS_CHOICES = (
        ('Running', 'Running'),
        ('AC', 'Accepted'),
        ('WA', 'Wrong Answer'),
        ('TLE', 'Time Limit Exceeded'),
        ('MLE', 'Memory Limit Exceeded'),
        ('CE', 'Compilation Error')
    )

    solution = models.FileField(verbose_name="Solution", upload_to=submission_directory_path)

    status = models.CharField(
        verbose_name="Status",
        choices=STATUS_CHOICES,
        default='Running',
        max_length=200
    )

    problem = models.ForeignKey(
        verbose_name="Problem",
        to=Problem,
        related_name='submissions',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        verbose_name="User",
        to=User,
        related_name='submissions',
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)


