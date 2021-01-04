from django import forms

from blog.models import Post,Comments


class BlogForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content']


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['Comment']
        widgets = {
            'Comment': forms.TextInput(
                attrs={'placeholder': 'Add a comment'}),
        }
        labels = {'Comment':''}
