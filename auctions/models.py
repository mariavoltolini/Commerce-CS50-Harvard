from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    status = models.BooleanField(default=True) 

    def __str__(self):
        return self.name

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30)
    description = models.TextField()
    image = models.CharField(max_length=255)
    price = models.FloatField()
    status = models.BooleanField(default=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="listingWatchlist")
    bid = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userBid")

    def __str__(self):
        return self.title

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="commentUser")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="commentListing")
    message = models.CharField(max_length=200)

    def __str__(self):
        return self.user

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    bid = models.FloatField(default=0)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="bidListing")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="bidUser")

    def __str__(self):
        return self.user