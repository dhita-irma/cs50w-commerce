from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.urls import reverse


class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing", blank=True, related_name="added_by")

class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Listing(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    start_price = models.DecimalField(max_digits=12, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    category = models.ManyToManyField(Category, blank=True, related_name="items")
    created_date = models.DateTimeField(default=timezone.now)
    image_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('listing-detail', kwargs={'pk': self.pk})

    def get_current_bid(self):
        bids = self.bids_offered.all()
        if bids:
            highest = bids.order_by('-price').first()
            return highest.price
        return self.start_price

    def get_winner(self):
        bids = self.bids_offered.all()
        if bids:
            highest = bids.order_by('-price').first()
            return highest.user
        return None


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids_offered")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="bids_placed")
    price = models.DecimalField(max_digits=12, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid {self.id} on {self.listing}"


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="comments_posted")
    body = models.TextField(max_length=250)
    posted_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.listing.title} - {self.user}"


