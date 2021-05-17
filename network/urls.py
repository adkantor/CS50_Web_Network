
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profiles/<int:user_id>", views.profiles, name="profiles"),

    # API Routes
    path("posts", views.create_post, name="posts"),
    path("follow/<int:user_id>", views.follow, name="follow"),
]

