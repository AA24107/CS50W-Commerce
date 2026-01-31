from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Bid, Comment, Listings


def index(request):
    
    return render(request, "auctions/index.html", {
        "listings": Listings.objects.filter(active=True)
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


def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        initial_price = int(request.POST["initial_price"])
        image_url = request.POST["image_url"]
        category = request.POST["category"].lower()
        
        active = "active" in request.POST

        Listings.objects.create(
            title=title,
            description = description,
            initial_price = initial_price,
            current_price = initial_price,
            image_url = image_url,
            category = category,
            active = active,
            owner = request.user
        )
        return HttpResponseRedirect(reverse("index"))
    

    return render(request, "auctions/create.html")


def listing(request, listing_id):
    listing = Listings.objects.get(id=listing_id)
    last_bid = listing.current_price
    is_watched = False
    message = None
    highest_bidder = Bid.objects.filter(listing=listing).order_by("-amount").first()

    if listing.active == False:
        if highest_bidder:
            f"{highest_bidder.bidder.username} has won the bid"

    if request.user.is_authenticated:
        is_watched = listing in request.user.watchlist.all()

    if request.method == "POST":
        if "place_bid" in request.POST:
            bid = request.POST.get("bid")
            if bid and last_bid < float(bid):
                Bid.objects.create(
                    listing=listing,
                    bidder=request.user,
                    amount=bid
                )
                listing.current_price = bid
                listing.save()
            else:
                message = "Please bid higher"
                print(message)

            return render(request, "auctions/listing.html", {
                "listing": listing,
                "bid": Bid.objects.filter(listing=listing).order_by("-amount"),
                "is_watched": is_watched,
                "comments": Comment.objects.filter(listing=listing),
                "user" : request.user,
                "message" : message
            })
        if "add_comment" in request.POST:
            comment_content = request.POST.get("comment")
            if comment_content:
                Comment.objects.create(
                    listing=listing,
                    commenter=request.user,
                    content=comment_content
                )
            return HttpResponseRedirect(
                reverse("listing", args=[listing.id])
            )

        if "watchlist" in request.POST and request.user.is_authenticated:
            if is_watched:
                request.user.watchlist.remove(listing)
            else:
                request.user.watchlist.add(listing)

            return HttpResponseRedirect(
                reverse("listing", args=[listing.id])
            )
        else:
            message = f"please log in"
        if 'close' in request.POST:
            if request.user == listing.owner and request.user.is_authenticated:
                listing.active = False
                listing.save()
                if highest_bidder:
                    message = f"{highest_bidder.bidder.username} has won the bid"
                else:
                    pass

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bid": Bid.objects.filter(listing=listing).order_by("-amount"),
        "is_watched": is_watched,
        "comments": Comment.objects.filter(listing=listing),
        "user" : request.user,
        "message" : message,
    })


def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "listings": request.user.watchlist.all()
    })


def categories(request):
    category = []
    listings = Listings.objects.all()
    for l in listings:
        category.append(l.category)
    categories = set(category)
    print(categories)
    return render(request, "auctions/categories.html", {
        "categories" : categories,
    })

def category_listing(request, category):
    listings = Listings.objects.filter(category=category) 
    return render(request, "auctions/category_listing.html", {
                  "listings": listings,
                  "category": category,
                  })