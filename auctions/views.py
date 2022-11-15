from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Category, User, Listing, Watchlist
from .forms import CommentForm, ListingForm, BiddingForm


def addToWatchlist(request):
    listing_pk = request.POST["listing"]
    listing = Listing.objects.get(id=listing_pk)
    Watchlist.objects.create(
        user = request.user,
        listing = listing
    )


def deleteFromWatchlist(request):
    listing_pk = request.POST["listing"]
    Watchlist.objects.filter(listing__id=listing_pk).delete()


def index(request):
    listings = Listing.objects.all()
    watchlist = None

    if request.user.is_authenticated:
        watchlist = Watchlist.objects.filter(user=request.user).values_list('listing', flat=True)

        if request.POST.get("delete"):
            deleteFromWatchlist(request)
            return HttpResponseRedirect(reverse("index"))
        
        if request.POST.get("add"):
            addToWatchlist(request)
            return HttpResponseRedirect(reverse("index"))

    context = {"listings": listings, 'watchlist': watchlist}
    return render(request, "auctions/index.html", context)


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


@login_required(login_url='login')
def listing(request, pk):
    submitted = False
    listing = Listing.objects.get(id=pk)
    comments = listing.comment_set.all()
    bids = listing.bid_set.all()
    bid_count = bids.count()
    if request.method =="POST":
        message_form = CommentForm(request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.listing = listing
            message.user = request.user
            message.save()
            return HttpResponseRedirect(f'/listing/{pk}/?submitted=True')
    else:
        message_form = CommentForm()
        if 'submitted' in request.GET:
            submitted = True
    context = {'listing': listing,'message_form': message_form,
    'submitted': submitted,'comments':comments,'bids':bids ,'bid_count':bid_count}
    return render(request, "auctions/listing.html", context)

@login_required(login_url='login')
def createListing(request):
    submitted = False
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            return HttpResponseRedirect('/create-listing?submitted=True')
    else:
        form = ListingForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, "auctions/listing_form.html", {
        "form": form, "submitted": submitted
    })


@login_required(login_url='login')
def updateListing(request, pk):
    submitted = False
    listing = Listing.objects.get(id=pk)
    
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f'/update-listing/{pk}/?submitted=True')
    else:
        form = ListingForm(instance=listing)
        if 'submitted' in request.GET:
            submitted = True
    context = {'form':form, 'submitted': submitted}
    return render(request, "auctions/listing_form.html", context)



def categories(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    listings = Listing.objects.filter(category__name__icontains=q)
    categories = Category.objects.all()
    watchlist = None

    if request.user.is_authenticated:
        watchlist = Watchlist.objects.filter(user=request.user).values_list('listing', flat=True)
        
        if request.POST.get("delete"):
            deleteFromWatchlist(request)
            return HttpResponseRedirect(reverse("categories"))
        
        if request.POST.get("add"):
            addToWatchlist(request)
            return HttpResponseRedirect(reverse("categories"))

    context = {'categories': categories,'listings': listings,'watchlist':watchlist}
    return render(request, "auctions/categories.html", context)


@login_required(login_url='login')
def bidding(request, pk):
    submitted = False
    error = False
    listing = Listing.objects.get(id=pk)

    if request.method == "POST":
        form = BiddingForm(request.POST)
        if form.is_valid():
            if float(request.POST["bid_value"]) <= float(listing.current_bid_value):
                return HttpResponseRedirect(f'/bidding/{pk}?error=True')
            else:
                listing.current_bid_value = request.POST["bid_value"]
                listing.save()
                bidding = form.save(commit=False)
                bidding.user = request.user
                bidding.listing = listing
                bidding.save()
                return HttpResponseRedirect(f'/bidding/{pk}?submitted=True')
    else:
        form = BiddingForm()
        if 'submitted' in request.GET:
            submitted = True
        if 'error' in request.GET:
            error = True
    context = {'listing':listing, 'form':form, 'submitted':submitted, 'error': error}
    return render(request, "auctions/bidding_form.html", context)


@login_required(login_url='login')
def watchlist(request):
    watchlist = Watchlist.objects.filter(user=request.user)

    if request.POST.get("delete"):
        deleteFromWatchlist(request)
        return HttpResponseRedirect(reverse("watchlist"))
        
    context = {'watchlist': watchlist }

    return render(request,"auctions/watchlist.html", context)