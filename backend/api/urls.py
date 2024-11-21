from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView
from api import views as api_views

urlpatterns = [
    
    path('user/token/', api_views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/register/', api_views.RegisterView.as_view(), name='auth_register'),
    path('user/profile/<user_id>/', api_views.ProfileView.as_view(), name='user_profile'),   
    path('post/category/list/', api_views.CategoryListAPIView.as_view()),
    path('post/category/posts/<category_slug>/', api_views.PostCategoryListAPIView.as_view()),   
    path('', api_views.home, name='home'),
    path('pages/', api_views.page, name='pages'),
    path('blog/', api_views.blog, name='blog'),
    path('login/', api_views.login, name='login'),
    path('register/', api_views.register, name='register'),
    path('baiviet/',api_views.blog,name='blog'),
    path('trangchu/',api_views.trangchu,name='trang_chu'),
    path('catalog/',api_views.catalog,name='catalog'),
    path('trang/',api_views.trang,name='trang'),
    path('vechungtoi/',api_views.vechungtoi,name='vechungtoi'),
    path('lienhe/',api_views.lienhe,name='lienhe'),
    path('baiviet',api_views.baiviet,name='baiviet'),
    path('add-post/', api_views.add_post, name='add_post'),
    path('post/<int:id>/', api_views.post_detail, name='post_detail'),
    path('profile/<str:username>/', api_views.user_profile, name='user_profile'),
    path('profile/',api_views.profile,name='profile'),

]


