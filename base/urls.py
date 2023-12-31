from django.urls import path
from . import views 


urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),

    path('', views.home, name="home"),
   
    path('posts/', views.posts, name="posts"),
    path('post/<slug:slug>/', views.post, name="post"),
    path('profile/', views.profile, name="profile"),

    path('create_post/', views.createPost, name="create_post"),
    path('update_post/<slug:slug>/', views.updatePost, name="update_post"),
    path('delete_post/<slug:slug>/', views.deletePost, name="delete_post"),

    path('send_email/', views.sendEmail, name="send_email"),


  
]