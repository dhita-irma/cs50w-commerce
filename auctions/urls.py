from django.urls import path

from .views import (
    ActiveListingView, 
    ListingDetailView, 
    ListingCreateView
)
from . import views

urlpatterns = [
    path("", ActiveListingView.as_view(), name="index"),
    path("listing/<int:pk>/", ListingDetailView.as_view(), name="listing-detail"),
    path("listing/new/", ListingCreateView.as_view(), name="listing-create"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories/", views.categories_index, name="categories-index"),
    path("categories/<str:category>", views.category_view, name="categories"),
]
