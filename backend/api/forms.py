from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=100, required=False)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", required=True)
    
    class Meta:
        model = User
        fields = ['username', 'password']
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'tags', 'category', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập tiêu đề'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Mô tả bài đăng'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập thẻ bài viết'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'comment']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên của bạn'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email của bạn'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Nội dung bình luận'}),
        }
        
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'full_name', 'bio', 'facebook', 'twitter']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Họ tên'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Về tôi', 'rows': 3}),
            'facebook': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Facebook URL'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Twitter URL'}),
        }