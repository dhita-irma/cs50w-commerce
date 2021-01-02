from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from django.views.generic import CreateView

from . import forms
from .models import *


def index(request):
    """Render and display the last 6 listings on the homepage."""

    categories = Category.objects.all()
    listings = Listing.objects.order_by('-created_date').all()

    return render(request, 'auctions/index.html', {
        "user": request.user,
        "listings":listings[:6]
    })

def active_listing(request):
    """Render page to display currently active listings, sorted from latest to oldest."""

    listings = Listing.objects.filter(is_active=True).order_by('-created_date')

    return render(request, 'auctions/listing_list.html', {
        "listings": listings,
        "title": "Active Listings",
    })


class ListingCreateView(LoginRequiredMixin, CreateView):
    """Generic display view to render Create Listing page"""

    model = Listing
    form_class = forms.ListingForm
    login_url = '/login/'

    # Set listing's seller to current logged-in user 
    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form) 


def listing_detail(request, pk):
    """Render page to display listing details"""

    listing = Listing.objects.get(pk=pk)
    listing_categories = listing.category.all()
    bids = Bid.objects.filter(listing=pk).order_by('-time') 

    user = request.user

    # Check if current listing is in user.watchlist
    is_watchlist = False
    if user.is_authenticated:
        if user.watchlist.filter(pk=pk).exists():
            is_watchlist = True


    return render(request, 'auctions/listing_detail.html', {
        'bid-form': forms.BidForm(),
        'comment-form': forms.CommentForm(),
        'is_watchlist': is_watchlist,
        'listing': listing,
        'listing_categories': listing_categories,
        'user': user,
        'bids': bids,
        'bids_len': len(bids)
    })


def listing_bid(request, pk):
    """Save new bids made by user to the Bid model in the database"""

    # Request has to be made via POST 
    if request.method == "POST":
        # If user is not logged in, redirect to login page
        if not request.user.is_authenticated:
            return redirect(reverse("login"))
        else:
            # Get and validate form data
            form = forms.BidForm(request.POST)
            if form.is_valid():
                price = form.cleaned_data['price']
                listing = Listing.objects.get(pk=pk)
                # Only accept bid if it's higher than current price, otherwise show error message
                if price > listing.get_current_bid():
                    bid = Bid(listing=listing, user=request.user, price=price)
                    bid.save()
                    messages.success(request, 'Bid successfully added.')
                    return redirect(reverse('listing-detail', args=[pk]))
                else:
                    messages.error(request, "Oops. Your bid has to be higher than the current one.")
                    return redirect(reverse('listing-detail', args=[pk]))
    else: 
        return render(request, 'auctions/error.html')


def listing_close(request, pk):
    """Close auction"""
    
    # Query requested listing
    listing = Listing.objects.get(pk=pk) 

    # Request has to be made via POST by user who owns the listing
    if request.method == 'POST' and request.user.username == listing.seller.username:
        listing.is_active = False
        listing.save()
        return redirect(reverse('index'))
    else: 
        return render(request, 'auctions/error.html')


def listing_comment(request, pk):
    """Post comment to a listing item"""

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect(reverse("login"))
        else:
            # Populate form object with data from POST request
            form = forms.CommentForm(request.POST)
            if form.is_valid():
                # Get comment body and query requested listing
                body = form.cleaned_data['body']
                listing = Listing.objects.get(pk=pk)

                # Create comment instance and save 
                comment = Comment(listing=listing, user=request.user, body=body)
                comment.save()
            return redirect(reverse('listing-detail', args=[pk]))
    else: 
        return render(request, 'auctions/error.html')


def category_list(request, category):
    """Render page to display listings in the requested category"""

    try:
        # Attempt to query listings with reequested category
        category = Category.objects.get(name=category)
        filtered_listings = Listing.objects.filter(category=category.id).order_by('-created_date')
        return render(request, "auctions/listing_list.html", {
            "title": category,
            "listings": filtered_listings,
        })     
    except:
        return render(request, "auctions/error.html")


@login_required(login_url='/login/')
def my_listings(request):
    """Render page to display listings that belongs to the currently logged in user"""

    my_listings = Listing.objects.filter(seller=request.user)
    return render(request, "auctions/listing_list.html", {
        "listings": my_listings,
        "title": "My Listings"
    })


@login_required(login_url='/login/')
def watchlist_add(request, pk):
    """Add a listing to Watchlist"""

    user = request.user
    listing = Listing.objects.get(pk=pk)
    user.watchlist.add(listing)
    user.save()

    listings = Listing.objects.filter(added_by=request.user.id)
    return redirect(reverse('listing-detail', args=[pk]))


@login_required(login_url='/login/')
def watchlist_remove(request, pk):
    """Remove a listing from Watchlist"""
    
    user = request.user
    user.watchlist.remove(pk)
    return redirect(reverse('listing-detail', args=[pk]))


@login_required(login_url='/login/')
def watchlist_view(request):
    """Render page to display listings in Watchlist of currently logged in user"""

    watchlist = Listing.objects.filter(added_by=request.user.id)
    return render(request, "auctions/listing_list.html", {
        "listings": watchlist,
        "title": "My Watchlist"
    })


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