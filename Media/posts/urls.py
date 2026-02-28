from django.urls import path
from . import views

urlpatterns = [
    path("add_post", views.add_post, name="add_post"),
    path("get_posts", views.get_all_posts, name="get_posts"),
    path("search", views.search_query, name="search"),
    path("profile", views.get_user_posts, name="profile"),
    path("delete", views.delete_post, name="delete"),
    path("edit", views.edit_post, name="edit"),
    path("like", views.like_unlike, name="like"),
    path("follow", views.follow_unfollow, name="follow"),
    path("get_followers", views.get_followers, name="followers")
    
]