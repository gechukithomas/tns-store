from .models import Blog
from django import forms

class AddBlogForm(forms.ModelForm):
    class Meta:
        model           = Blog
        fields          = ['category', 'variation', 'title', 'short_description', 'description', 'image']
