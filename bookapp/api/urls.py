from django.urls import path, include
from . import views 
from rest_framework.routers import DefaultRouter 

routers = DefaultRouter()
routers.register("authors", views.AuthorView, basename="author")
routers.register("category", views.CategoryView, basename="category")

urlpatterns = [
    path("all-books/", views.BookListView.as_view(), name="books"),
    path("book-detail/<str:slug>/", views.BookDetailView.as_view(), name="book-detail"),
    path("", include(routers.urls)),
    path("review/<int:pk>/", views.ReviewDetail.as_view(), name="individual-reviews"),
    path("book-detail/<str:slug>/reviews/", views.ReviewList.as_view(), name="review-list"), 
    path("book-detail/<str:slug>/reviews/add/", views.ReviewCreateView.as_view(), name="review-create"),
    path("reviews/<str:username>/", views.UserReviews.as_view(), name="user-reviews")
]

