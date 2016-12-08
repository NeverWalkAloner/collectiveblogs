from pagedown.widgets import PagedownWidget
from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget, label='Текст')

    class Meta:
        model = Post
        fields = ['title', 'content', 'blog']