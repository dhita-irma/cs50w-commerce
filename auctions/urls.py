from django.urls import path

from .views import (
    # ActiveListingView, 
    ListingCreateView,
    ListingUpdateView,
    ListingDeleteView,
)
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    
    path("listing/", views.active_listing, name="active"),
    path("listing/new/", ListingCreateView.as_view(), name="listing-create"),
    path("listing/<int:pk>/", views.listing_detail, name="listing-detail"),
    path("listing/<int:pk>/delete/", ListingDeleteView.as_view(), name="listing-delete"),
    path("listing/<int:pk>/bid/", views.listing_bid, name="listing-bid"),
    path("listing/<int:pk>/comment/", views.listing_comment, name="listing-comment"),
    path("listing/<int:pk>/close/", views.listing_close, name="listing-close"),
    
    path("my_listings/", views.my_listings, name="my-listings"),

    path("watchlist/", views.watchlist_view, name="watchlist"),
    path("listing/<int:pk>/watchlist/", views.watchlist_add, name="watchlist-add"),
    path("listing/<int:pk>/watchlist/remove/", views.watchlist_remove, name="watchlist-remove"),

    path("categories/", views.category_index, name="category-index"),
    path("categories/<str:category>", views.category_list, name="category-list"),
]
