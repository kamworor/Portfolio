from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Post

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

        widgets = {
            'tags':forms.CheckboxSelectMultiple(),
        }

    
    