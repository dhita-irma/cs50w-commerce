from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.views.generic import(
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView,
)

from . import forms
from .models import *


class ActiveListingView(ListView):
    model = Listing
    context_object_name = 'listings' 

    # Order listings from latest to oldest
    ordering = ['-created_date'] 


class ListingDetailView(DetailView):
    model = Listing


class ListingCreateView(LoginRequiredMixin, CreateView):
    model = Listing
    form_class = forms.ListingForm
    login_url = '/login/'
    # TODO: redirect user back to /listing/new/ after login

    # Set listing's seller to current logged-in user 
    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form) 


class ListingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Listing
    form_class = forms.ListingForm
    login_url = '/login/'
    # TODO: redirect user back to /listing/new/ after login

    # Set listing's seller to current logged-in user 
    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form) 

    def test_func(self):
        # Get the current listing object
        listing = self.get_object()

        # Check if current user is the seller of listing
        if self.request.user == listing.seller:
            return True
        return False 


class ListingDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Listing

    def test_func(self):
        # Get the current listing object
        listing = self.get_object()

        # Check if current user is the seller of listing
        if self.request.user == listing.seller:
            return True
        return False 


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def category_view(request, category):
    try:
        category = Category.objects.get(name=category)
        category_id = category.id
        filtered_listings = Listing.objects.filter(category=category_id)
        return render(request, "auctions/category.html", {
            "filtered_listings": filtered_listings
        })     
    except:
        return render(request, "auctions/error.html")

def categories_index(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories-index.html", {
        "categories": categories
    })

@login_required(login_url='/login/')
def watchlist_view(request):
    watchlist = Listing.objects.filter(added_by=request.user.id)
    return render(request, "auctions/listing_list.html", {
        "listings": watchlist
    })

@login_required(login_url='/login/')
def watchlist_add(request, pk):
    user = request.user
    listing = Listing.objects.get(pk=pk)
    user.watchlist.add(listing)
    user.save()

    listings = Listing.objects.filter(added_by=request.user.id)
    return render(request, "auctions/listing_list.html", {
        "listings": listings
    })

