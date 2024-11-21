from django.shortcuts import render
from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import *

from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.db.models import Sum
# Restframework

from rest_framework import status
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
 
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from datetime import datetime

# Others
import json
import random

# Custom Imports

from api import serializer as api_serializer
from api import models as api_models

# regiter and trang chủ

def index(request):  
    return render(request,"base.html")
def trangchu(request):
    trending_posts=Post.objects.all()
    categories=Category.objects.all()
    popular_posts=Post.objects.all()
    context={
        'trending_posts':trending_posts,
        'categories':categories,
        'popular_posts':popular_posts,
    }
    return render(request,"trangchu.html",context)



def blog(request):
    return render(request,'blog.html')
def catalog(request):
    return render(request,"catalog.html")
def vechungtoi(request):
    return render(request,'vechungtoi.html')
def lienhe(request):
    return render(request,'lienhe.html')


def trang(request):
    return render(request,'trang.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)       
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Tài khoản {username} đã được tạo thành công!')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Chào mừng {user.full_name} quay lại!')
                return redirect('trang_chu')  
            else:
                messages.error(request, 'Email hoặc mật khẩu không chính xác.')
        else:
            messages.error(request, 'Có lỗi xảy ra trong quá trình đăng nhập.')
    else:
        form = LoginForm()
    return render(request, 'loggin.html', {'form': form})

def baiviet(request):
    baiviet=Post.objects.all()
    return render(request,'baiviet.html',{'baiviet':baiviet}) 


@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.profile = request.user.profile
            post.save()
            messages.success(request, 'Bài đăng đã được tạo thành công!')
            return redirect('baiviet', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'add_post.html', {'form': form})

def post_detail(request,id):
    post = get_object_or_404(Post, id=id)
    post.view += 1
    post.save()
    comments = post.comments()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Bình luận của bạn đã được thêm!')
            return redirect('post_detail', id=post.id)
    else:
        form = CommentForm()
    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'form': form})

    
def user_profile(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    user_posts = Post.objects.filter(user=profile.user).order_by('-date')  # Lấy bài viết của người dùng

    context = {
        'profile': profile,
        'user_posts': user_posts,
    }
    return render(request, 'profile.html', context)


def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Hồ sơ đã được cập nhật thành công!")
            return redirect('profile_view')
        else:
            messages.error(request, "Vui lòng kiểm tra lại thông tin.")
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'user_profile.html', {'form': form, 'profile': profile})



def notifications(request):
    notifications = Notification.objects.filter(user=request.user, seen=False)
    for notification in notifications:
        notification.seen = True
        notification.save()

    return render(request, "notifications.html", {"notifications": notifications}) 
 
def home(request):
    return render(request, 'home.html')

def page(request):
    return render(request, 'page.html')

def blog(request):
    return render(request, 'blog.html')

def register(request):
    return render(request, 'register.html')

#------------------------------------------------
class MyTokenObtainPairView(TokenObtainPairView):
    # Here, it specifies the serializer class to be used with this view.
    serializer_class = api_serializer.MyTokenObtainPairSerializer

# This code defines another DRF View class called RegisterView, which inherits from generics.CreateAPIView.
class RegisterView(generics.CreateAPIView):
    # It sets the queryset for this view to retrieve all User objects.
    queryset = api_models.User.objects.all()
    # It specifies that the view allows any user (no authentication required).
    permission_classes = (AllowAny,)
    # It sets the serializer class to be used with this view.
    serializer_class = api_serializer.RegisterSerializer
    
    
class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = api_serializer.ProfileSerializer

    def get_object(self):
        user_id = self.kwargs['user_id']

        user = api_models.User.objects.get(id=user_id)
        profile = api_models.Profile.objects.get(user=user)
        return profile

class CategoryListAPIView(generics.ListAPIView):
    serializer_class = api_serializer.CategorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return api_models.Category.objects.all()

class PostCategoryListAPIView(generics.ListAPIView):
    serializer_class = api_serializer.PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        category_slug = self.kwargs['category_slug'] 
        category = api_models.Category.objects.get(slug=category_slug)
        return api_models.Post.objects.filter(category=category, status="Active")