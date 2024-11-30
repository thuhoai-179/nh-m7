from django.shortcuts import render
from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import *
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Sum
# Restframework
from rest_framework import status
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
 
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from datetime import datetime
from api import serializer as api_serializer
from api import models as api_models

# regiter and trang chủ

def index(request):  
    print(request.user)
    return render(request,"base.html")
def trangchu(request):
    trending_posts=Post.objects.all().order_by('-view')[:10]
    categories=Category.objects.all()
    popular_posts=Post.objects.all().order_by('-likes')[:10]
    context={
        'trending_posts':trending_posts,
        'categories':categories,
        'popular_posts':popular_posts,
    }
    return render(request,"trangchu.html",context)

def danhmuc(request):
    categories=Category.objects.all()
    return render(request,'danhmuc.html',{'categories':categories})

def test_code(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.profile = request.user.profile
            post.save()
            messages.success(request, 'Bài đăng đã được tạo thành công!')
            return redirect('post_detail', id=post.id)
    else:
        form = PostForm()
    return render(request, 'test_code.html', {'form': form})


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
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Tài khoản {user.username} đã được tạo thành công!')
            return redirect('login')  # Đảm bảo URL 'login' được định nghĩa
    return render(request, 'register.html', {'form': form})

def user_login(request):
    form = AuthenticationForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Chào mừng {user.username} quay lại!')
            return redirect('trang_chu')  
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

def baiviet(request):
    baiviet=Post.objects.all()
    return render(request,'baiviet.html',{'baiviet':baiviet}) 

def post_details(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.post = post
            instance.save()
            return redirect('baivietchitiet', id=post.id)

    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'baivietchitiet.html', context)



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
            return redirect('post_detail', id=post.id)
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
            comment.user = request.user
            reply_id = request.POST.get('reply_id')

            if reply_id:
                comment.reply = Comment.objects.get(id=reply_id)
            comment.save()

            messages.success(request, 'Bình luận đã được thêm thành công!')
            return redirect('post_detail', id=post.id)
    else:
        form = CommentForm()

    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'form': form})

@login_required
def edit_post(request,id):
    post = get_object_or_404(Post, id=id)   
    if request.method == "POST":
        form = Edit_PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("baiviet") 
    else:
        form = Edit_PostForm(instance=post)
    
    return render(request, "edit_post.html", {"form": form, "post": post})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'likes_count': post.likes.count()})

def category_post_list(request,id):
    category = get_object_or_404(Category, id=id)
    posts = Post.objects.filter(category=category, status="Active").order_by("-date")   
    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'category_post_list.html', context)



@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully!")
            return redirect('danhmuc')
    else:
        form = CategoryForm()
    return render(request, 'category_create.html', {'form': form, 'action': 'Create'})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, "Category deleted successfully!")
        return redirect('danhmuc')
    return render(request, 'category_confirm_delete.html', {'category': category})

@login_required
def  post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully!")
        return redirect('baiviet')
    return render(request, 'post_confirm_delete.html', {'post': post})


@login_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully!")
            return redirect('danhmuc')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category_edit.html', {'form': form, 'action': 'Edit'})   
    
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

    
class LikePostAPIView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'post_id': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    )
    def post(self, request):
        try:
            # Lấy dữ liệu từ request
            user_id = request.data.get('user_id')
            post_id = request.data.get('post_id')

            # Kiểm tra dữ liệu đầu vào
            if not user_id or not post_id:
                raise ValidationError("Both 'user_id' and 'post_id' are required.")

            # Truy vấn người dùng và bài viết
            user = get_object_or_404(api_models.User, id=user_id)
            post = get_object_or_404(api_models.Post, id=post_id)

            # Kiểm tra trạng thái thích/bỏ thích
            if post.likes.filter(id=user.id).exists():
                # Nếu đã thích, bỏ thích
                post.likes.remove(user)
                return Response({"message": "Post Disliked"}, status=status.HTTP_200_OK)
            else:
                # Nếu chưa thích, thêm lượt thích
                post.likes.add(user)

                # Tạo thông báo cho tác giả bài viết
                api_models.Notification.objects.create(
                    user=post.user,
                    post=post,
                    type="Like",
                )

                return Response({"message": "Post Liked"}, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)