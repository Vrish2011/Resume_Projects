from django.urls import path
from . import views

urlpatterns = [
    path("register", views.register_template, name="register"),
    path("login", views.login_template, name="login"),
    path("", views.home_template, name="home"),
    path("search", views.search_template, name="search"),
    path("profile", views.profile_template, name="profile"),
    path("followers", views.followers, name="followers")
]