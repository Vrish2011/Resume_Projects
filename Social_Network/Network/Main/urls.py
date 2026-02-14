from django.urls import path
from . import views
urlpatterns = [
    path("home", views.home, name="home"),
    path("login", views.login_template, name="login"),
    path("register", views.register_template, name="register"),
    path("Home", views.home_template, name="home"),
    path("add_post", views.add_post, name="add_post")

    
]