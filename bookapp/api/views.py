from django.shortcuts import get_object_or_404
from rest_framework.response import Response 
from rest_framework.views import APIView 
from rest_framework import generics, viewsets, filters, status 
from rest_framework.validators import ValidationError 
from django.db.models import Avg 
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend


from bookapp.models import *
from .serializers import *
from .permissions import AdminOrAuthenticatedUser, ReviewUserOnly, AdminOrReadOnly
from .paginators import WatchListPagination

# Create your views here.
class BookListView(generics.ListCreateAPIView):
    
    permission_classes = [AdminOrAuthenticatedUser]
    queryset = Book.objects.all()
    serializer_class = BookSerializer 
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = [
                        "title", 
                        "author__first_name", 
                        "author__last_name", 
                        "author__middle_name", 
                        "category__name", 
                        "published_countries__name"
                       ]
    search_fields = [
                        "title", 
                        "author__first_name", 
                        "author__last_name", 
                        "author__middle_name", 
                        "category__name", 
                        "published_countries__name",
                        "published_countries__code"
                    ]
    ordering_fields = ["average_rating"]
    pagination_class = WatchListPagination
    

class BookDetailView(APIView):
    permission_classes = [AdminOrAuthenticatedUser]
    
    def get_object(self, slug):
        return get_object_or_404(Book, slug=slug) 
    
    def get(self, request, slug):
        book = self.get_object(slug)
        serializer = BookSerializer(book)
        return Response(serializer.data) 
    
    def put(self, request, slug):
        book = self.get_object(slug)
        serializer = BookSerializer(book, data=request.data)  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, slug):
       book = self.get_object(slug)
       book.delete()
       msg = "Book successfully deleted"
       return Response(msg, status=status.HTTP_204_NO_CONTENT)


class AuthorView(viewsets.ViewSet):
    lookup_field = "first_name"
    permission_classes = [AdminOrAuthenticatedUser]
    
    def list(self, request):
        queryset = Author.objects.all()
        serializer = AuthorSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data) 

    def create(self, request):
        serializer = AuthorSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, first_name):
        queryset = get_object_or_404(Author, first_name=first_name)
        serializer = AuthorSerializer(queryset, context={"request": request})
        return Response(serializer.data)
        
    def update(self, request, first_name):
        queryset = get_object_or_404(Author, first_name=first_name)
        serializer = AuthorSerializer(queryset, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, first_name):
        queryset = get_object_or_404(Author, first_name=first_name)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer 
    
    def get_queryset(self):
        slug = self.kwargs["slug"]
        return Review.objects.filter(book__slug=slug)
    

class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer 
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        slug = self.kwargs["slug"]
        book = Book.objects.get(slug=slug)
        review_user = self.request.user
        review = Review.objects.filter(book=book, review_user=review_user)
        if review.exists():
            raise ValidationError("Sorry, but you have already submitted a review for this book !")
        else:   
            serializer.save(book=book, review_user=review_user)
            book_review = Review.objects.filter(book=book)
            average_rating = book_review.aggregate(Avg("rating"))
            no_reviews = book_review.count()
            book.average_rating = average_rating["rating__avg"]
            book.no_reviews = no_reviews 
            book.save()


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [ReviewUserOnly]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    
class UserReviews(generics.ListAPIView):
    serializer_class = ReviewSerializer 
    
    def get_queryset(self):
        username = self.kwargs["username"]
        queryset = Review.objects.filter(review_user__username=username)
        return queryset 
        
class CategoryView(viewsets.ViewSet):
    permission_classes = [AdminOrReadOnly] 
    lookup_field = 'name'
    
    def list(self, request):
        queryset = Category.objects.all() 
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, name):
        queryset = get_object_or_404(Category, name=name)
        serializer = CategorySerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, name):
        queryset = get_object_or_404(Category, name=name)
        serializer = CategorySerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, name):
        queryset = get_object_or_404(Category, name=name)
        queryset.delete()
        return Response(tatus=status.HTTP_204_NO_CONTENT)