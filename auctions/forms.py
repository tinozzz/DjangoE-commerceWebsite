from django.forms import ModelForm
from .models import Listing, Bid, Comment, Watchlist


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = '__all__'
        exclude = ['user','watchlist']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class BiddingForm(ModelForm):
    class Meta:
        model  = Bid
        fields = ['bid_value']
