from time import sleep

from django.db.models.signals import post_save
from django.dispatch import receiver

from learning.judge import compile_submission
from learning.models import Submission


@receiver(post_save, sender=Submission)
def compile_solution(sender, instance, created, **kwargs):
    if created:
        compile_submission(instance)

