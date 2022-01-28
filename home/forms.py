from django import forms
from django.forms import widgets
from .models import Blog, Comment

class Edit_blog(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ("title","desc")

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("name", "body")

        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control'}),
            'body' : forms.Textarea(attrs={'class': 'form-control'})
        }