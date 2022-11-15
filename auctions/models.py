from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=200)
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64, null=True, blank=True)
    current_bid_value = models.DecimalField(null=True, decimal_places=2, max_digits=7)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return f"title: {self.title}, description: {self.description}, "\
            f"img: {self.image}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return f"{self.user}: {self.listing.title}"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid_value = models.DecimalField(null=True, decimal_places=2, max_digits=7)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        
    def __str__(self):
        return f"Bid for {self.listing.title} $:{self.bid_value}, Created by:{self.user} on {self.created}"

        
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return f"{self.user}: {self.content[0:50]}"
        