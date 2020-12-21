from django import forms
from learning.models import Submission


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = [ 'solution']