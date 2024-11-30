from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView
from api import views as api_views

urlpatterns = [
     
    path('', api_views.user_login, name='user_login'),
    path('pages/', api_views.page, name='pages'),
    path('blog/', api_views.blog, name='blog'),
    path('login/', api_views.user_login, name='login'),
    path('logout/', api_views.user_logout, name='logout'),
    path('register/', api_views.register, name='register'),
    path('trangchu/',api_views.trangchu,name='trang_chu'),
    path('catalog/',api_views.catalog,name='catalog'),
    path('trang/',api_views.trang,name='trang'),
    path('vechungtoi/',api_views.vechungtoi,name='vechungtoi'),
    path('lienhe/',api_views.lienhe,name='lienhe'),
    path('baiviet/',api_views.baiviet,name='baiviet'),
    path('add-post/', api_views.add_post, name='add_post'),
    path('post/<int:id>/', api_views.post_detail, name='post_detail'),
    path('edit_post/<int:id>/', api_views.edit_post, name="edit_post"),
    path('post/<int:pk>/delete/', api_views.post_delete, name='post_delete'),
    path('profile/<str:username>/', api_views.user_profile, name='user_profile'),
    path('profile/',api_views.profile,name='profile'),
    path('category/<int:id>/', api_views.category_post_list, name='category_post_list'),
    path('categories/create/',api_views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', api_views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', api_views.category_delete, name='category_delete'),
    path('baivietchitiet/<int:id>/', api_views.post_details, name='baivietchitiet'),
    path('danhmuc/',api_views.danhmuc,name='danhmuc'),
    path('test_code/',api_views.test_code,name='test_code'),
    path('post/like-post/', api_views.LikePostAPIView.as_view()),
]


