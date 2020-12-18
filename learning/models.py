from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User


class Tutorial(models.Model):
    title = models.CharField(max_length=50, blank=True)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    problem_ids = models.JSONField(verbose_name="Problem Id's", default=list)


class Score(models.Model):
    learner = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)


class Problem(models.Model):
    name = models.CharField(max_length=100)
    statement = models.TextField()
    input_section = models.TextField()
    output_section = models.TextField()
    time_limit = models.IntegerField(verbose_name='Time Limit', default=1)
    memory_limit = models.PositiveIntegerField(verbose_name='Memory Limit', default=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name