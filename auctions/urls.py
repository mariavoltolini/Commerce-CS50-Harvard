from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.addListing, name="add"),
    path("submitAdd", views.submitAdd, name="submitAdd"),
    path("filter", views.filter, name="filter"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("watchlistAdd/<int:id>", views.watchlistAdd, name="watchlistAdd"),
    path("watchlistRemove/<int:id>", views.watchlistRemove, name="watchlistRemove"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("addComment/<int:id>", views.addComment, name="addComment"),
    path("addBid/<int:id>", views.addBid, name="addBid"),
    path("closeListing/<int:id>", views.closeListing, name="closeListing"),
    path("winningBid", views.winningBid, name="winningBid"),
]
