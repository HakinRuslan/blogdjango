from .models import *
from django.forms import ModelForm, TextInput, DateTimeInput, Select, ClearableFileInput, FileField, FileInput
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from django.contrib.auth.forms import UserCreationForm
from django import forms

class CreatePost(forms.ModelForm):
    class Meta:
        model = Blogpost
        fields = ['title', 'desc']


        widgets = {
            'desc': TextInput(attrs={
                'placeholder': 'Текст поста',
            }),
            'title': TextInput(attrs={
                'placeholder': 'Название вашего поста',
            }),
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment_on_post
        fields = ['desc']
    
        widgets = {
            'desc': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Коментарий',
            }),
        }

class ReplyForm(ModelForm):
    class Meta:
        model = ReplyOnComm
        fields = ['desc']
    
        widgets = {
            'desc': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ответ',
            }),
        }

class registrationuser(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email", )