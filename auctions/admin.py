from django.contrib import admin

from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ("id",)

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "seller")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "item", "bidder", "price") 


admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Category)
admin.site.register(Bid, BidAdmin)
