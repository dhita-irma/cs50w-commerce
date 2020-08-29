from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings/<int:listing_id>", views.listing_item, name="listings"),
    path("categories/", views.categories_index, name="categories_index"),
    path("categories/<str:category>", views.category_view, name="categories")
]
