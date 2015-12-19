# forms.py
from django import forms

from .models import Photo
from .models import Comment


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('image', 'description', )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )
