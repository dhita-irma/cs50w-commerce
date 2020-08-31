from django.urls import path

from .views import (
    ActiveListingView, 
    ListingDetailView, 
    ListingCreateView,
    ListingUpdateView,
    ListingDeleteView,
)
from . import views

urlpatterns = [
    path("", ActiveListingView.as_view(), name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("listing/<int:pk>/", ListingDetailView.as_view(), name="listing-detail"),
    path("listing/<int:pk>/update/", ListingUpdateView.as_view(), name="listing-update"),
    path("listing/<int:pk>/delete/", ListingDeleteView.as_view(), name="listing-delete"),
    path("listing/<int:pk>/watchlist/", views.watchlist_add, name="watchlist-add"),
    path("watchlist/", views.watchlist_view, name="watchlist"),
    path("listing/new/", ListingCreateView.as_view(), name="listing-create"),
    path("categories/", views.categories_index, name="categories-index"),
    path("categories/<str:category>", views.category_view, name="categories"),
]
