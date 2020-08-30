from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.urls import reverse


class User(AbstractUser):
    watchlist = models.ForeignKey("Listing", models.SET_NULL, blank=True, null=True)


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

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('listing-detail', kwargs={'pk': self.pk})


class Bid(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids_offered")
    bidder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="bids_placed")
    price = models.DecimalField(max_digits=12, decimal_places=2)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Bid {self.id} on {self.item}"


class Comment(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="comments_posted")
    posted_date = models.DateTimeField(default=timezone.now)

