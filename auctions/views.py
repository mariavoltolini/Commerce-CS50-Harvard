from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid


def index(request):
    all = Listing.objects.filter(status=True)
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "all": all,
        "categories": categories
    })

def filter(request):
    if request.method == "GET":
        if(request.GET['category'] != ''):
            all = Listing.objects.filter(status=True, category=request.GET['category'])
        else:
            all = Listing.objects.filter(status=True)
            
        categories = Category.objects.all()
        return render(request, "auctions/index.html", {
            "all": all,
            "categories": categories
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

def addListing(request):
    categories = Category.objects.all()
    return render(request, "auctions/add.html", {
        "categories": categories
    })

def submitAdd(request):
    category = Category.objects.get(id=request.POST['category'])
    newListing = Listing(
        title=request.POST['title'],
        description=request.POST['description'],
        image=request.POST['image'],
        price=request.POST['price'],
        user=request.user,
        category=category
    )
    newListing.save()
    return HttpResponseRedirect(reverse("index"))

def listing(request, id):
    listing = Listing.objects.get(id=id)
    watchlist = request.user in listing.watchlist.all()
    comments = Comment.objects.filter(listing=id)
    user = request.user
    return render(request, "auctions/listing.html", {
            "listing": listing,
            "watchlist": watchlist,
            "comments": comments,
            "user": user
    })

def watchlistAdd(request, id):
    listing = Listing.objects.get(id=id)
    listing.watchlist.add(request.user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def watchlistRemove(request, id):
    listing = Listing.objects.get(id=id)
    listing.watchlist.remove(request.user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def watchlist(request):
    user = request.user
    all = Listing.objects.filter(status=True, watchlist=user)
    count = len(Listing.objects.filter(status=True, watchlist=user))
    return render(request, "auctions/watchlist.html", {
            "all": all,
            "count": count,
    })

def addComment(request,id):
    if request.method == "GET":
        listing = Listing.objects.get(id=id)
        return render(request, "auctions/comment.html", {
            "listing": listing,
        })
    elif request.method == "POST":
        listing = Listing.objects.get(id=id)
        newComment = Comment(
            listing=listing,
            message=request.POST['comment'],
            user=request.user,
        )
        newComment.save()
        return HttpResponseRedirect(reverse("listing", args=(id, )))

def addBid(request,id):
    if request.method == 'POST':
        listing = Listing.objects.get(id=id)
        bid = request.POST['bid']
        if float(listing.price) < float(bid):
            newBid = Bid(
                bid=float(bid),
                listing=listing,
                user=request.user,
            )
            newBid.save()

            listing.bid = request.user
            listing.price = float(bid)
            listing.save()

            return HttpResponseRedirect(reverse("listing", args=(id, )))
        else:
            watchlist = request.user in listing.watchlist.all()
            comments = Comment.objects.filter(listing=id)
            message = 'Amount less than the minimum bid!'
            user = request.user
            return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "watchlist": watchlist,
                    "comments": comments,
                    "message": message,
                    "user": user
            })
    
def closeListing(request,id):
    listing = Listing.objects.get(id=id)
    listing.status = False
    listing.save()
    
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def winningBid(request):
    user = request.user
    all = Listing.objects.filter(status=False, bid=user)
    return render(request, "auctions/winning.html", {
        "all": all,
    })

            


