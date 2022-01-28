from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name="index"),
    path('about', views.about, name="about"),
    path('register', views.registerUser, name="register"),
    path('login', views.loginUser, name="login"),
    path('logout', views.logoutUser, name="logout"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('post_blog', views.post_blog, name="post_blog"),
    path('display/<int:id>', views.displayblog, name="display"),
    path('display/editblog/<int:id>', views.editblog, name="editblog"),
    path('display/deleteblog/<int:id>', views.deleteblog, name="deleteblog"),
    path('like/<int:pk>', views.postlike, name="blog_like"),
    path('display/<int:id>/comment', views.Addcomment.as_view(), name="add_comment"),
    path('search', views.search, name="search"),

]