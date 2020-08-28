from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    watchlist = models.ForeignKey(
        "Listing",
        models.SET_NULL,
        blank=True,
        null=True,
    )

class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    start_price = models.DecimalField(max_digits=12, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    start_date = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(
        Category, 
        models.SET_NULL,
        blank=True, 
        null=True, 
        related_name="items"
    )
    #TODO: end_date

    def __str__(self):
        return f"{self.title}"

#TODO:
# class Bid(models.Model):
#     item = models.ManyToOneRel(Listing, related_name="item")
#     price = models.DecimalField(max_digits=12, decimal_places=2)
#     time = models.DateTimeField(default=timezone.now)

# class Comment(models.Model):
#     # content = models.TextField()
#     # user = pass
#     # created_time = pass
#     # edited_time = pass
#     pass


