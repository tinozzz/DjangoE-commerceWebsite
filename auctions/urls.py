from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create-listing/", views.createListing, name="create-listing"),
    path("update-listing/<str:pk>/", views.updateListing, name="update-listing"),
    path("listing/<str:pk>/", views.listing, name="listing"),
    path("categories/", views.categories, name="categories"),
    path("bidding/<str:pk>/", views.bidding, name="bidding"),
    path("watchlist", views.watchlist, name="watchlist"),
]
