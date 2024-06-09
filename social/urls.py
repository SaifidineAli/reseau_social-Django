from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('new/', views.new_post, name='new_post'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('users/', views.user_list, name='user_list_to_follow'),
    path('notifications/', views.notifications, name='notifications'),
]