from django import forms
from chat.models import Messages


class NewMessageForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ['message']
        labels = {'message':''}