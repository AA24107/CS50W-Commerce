from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listings', blank=True, related_name ='watchlisted_by')

class Listings(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    initial_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")


class Bid(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="bids", null=True, blank=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"${self.amount} by {self.bidder.username} on {self.listing.title}"

class Comment(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="comments", null=True, blank= True)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.commenter.username} on {self.listing.title}"
    
