from django.forms import SlugField
from rest_framework.test import APITestCase 
from rest_framework import status
from .models import Book, Author, Category, Country, Review
from django.urls import reverse 
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

# Create your tests here.

class ModelSetup:
    
    def common_model_setup(self):
        self.category1 = Category.objects.create(name="Folklore")
        self.category2 = Category.objects.create(name="History")
        self.author = Author.objects.create(first_name="Kerry", last_name="Onyeogo", middle_name="Nwaka")
        self.author2 = Author.objects.create(first_name="Preston", last_name="Clement", middle_name="Chizi")
        self.country1 = Country.objects.create(name="Germany", code="DE")
        self.country2 = Country.objects.create(name="United Kingdom", code="UK")
        self.user = User.objects.create_user(username="exampleuser", email="example@gmail.com", password="Akpororo1")
        self.book = Book.objects.create(
                                        title="No longer at ease", 
                                        author=self.author, 
                                        is_bestselling=False, 
                                        description="No longer at ease by Preston"
                                        )
        self.book.published_countries.add(self.country1)
        self.book.published_countries.add(self.country2)
        self.book.save()
        refresh = RefreshToken.for_user(self.user)
        access_token = refresh.access_token
        self.client.credentials(HTTP_AUTHORIZATION= f"Bearer {access_token}")
        
class AuthorTestCase(ModelSetup, APITestCase):
    
    def setUp(self):
        return super().common_model_setup()
        
    def test_author_list(self):
        response = self.client.get(reverse("author-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)  
        
    def test_add_author(self):
        data = {
            "first_name": "Kerry",
            "last_name": "Onyeogo",
            "middle_name": "Nwaka"
        }
        response = self.client.post(reverse("author-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_get_individual_author(self):
        response = self.client.get(reverse("author-detail", args=[self.author.first_name]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)  
        
    def test_update_individual_author(self):
        data = {
            "first_name": "Kerry-updated",
            "last_name": "Onyeogo-updated",
            "middle_name": "Nwaka-updated"
        }
        response = self.client.put(reverse("author-detail", args=[self.author.first_name]), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_delete_individual_author(self):
        response = self.client.delete(reverse("author-detail", args=[self.author.first_name]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        

class CategoryTestCase(ModelSetup, APITestCase):
    
    def setUp(self):
        return super().common_model_setup()
        
    def test_create_category(self):
        data = {
            "name": "Tales"
        }
        response = self.client.post(reverse("category-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_get_category_list(self):
        response = self.client.get(reverse("category-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_individual_category(self):
        response = self.client.get(reverse("category-detail", args=[self.category1.name]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)  
        
    def test_update_individual_category(self):
        data = {
            "name": "History"
        }
        response = self.client.put(reverse("category-detail", args=[self.category1.name]), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_delete_individual_category(self):
        response = self.client.delete(reverse("category-detail", args=[self.category2.name]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
class BookTestCase(ModelSetup, APITestCase):

    def setUp(self):
        return super().common_model_setup()
        
    def test_book_create(self):
        data = {
            "title": "Son of Eve",
            "author": self.author,
            "published_countries": [self.country1, self.country2],
            "category": [self.category1, self.category2],
            "is_bestselling": True,
            "description": "Nice Book"
        }
        response = self.client.post(reverse("books"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_book_update(self):
        data = {
            "title": "Son of Abel",
            "author": self.author2,
            "published_countries": [self.country2],
            "category": [self.category1],
            "is_bestselling": True,
            "description": "A book about love"
        }
        response = self.client.put(reverse("book-detail", args=[self.book.slug]), data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) 
        
    
    def test_get_book_list(self):
        response = self.client.get(reverse("books"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_individual_book(self):
        response = self.client.get(reverse("book-detail", args=[self.book.slug]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_delete_individual_book(self):
        response = self.client.delete(reverse("book-detail", args=[self.book.slug]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
        
class ReviewTestCase(ModelSetup, APITestCase):
    
    def setUp(self):
        return super().common_model_setup()
        
    def test_review_create(self):
        data = {
            "rating": 3.5,
            "body": "trash book",
        }
        response = self.client.post(reverse("review-create", args=[self.book.slug]), data)
        json_data = response.json()
        review = Review.objects.get(book__title=json_data.get("book_title"))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(review.book.no_reviews, 1)
        self.assertEqual(review.book.average_rating, 3.5)
        # Try to create another review, we should get a 400 bad request error
        response = self.client.post(reverse("review-create", args=[self.book.slug]), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
    def test_review_create_unauth(self):
        self.client.force_authenticate(user=None)
        data = {
            "rating": 3.5,
            "body": "trash book",
        }
        response = self.client.post(reverse("review-create", args=[self.book.slug]), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_reviews_by_book(self):
        response = self.client.get(reverse("review-list", args=[self.book.slug]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_reviews_by_auth_user(self):
        response = self.client.get(reverse("user-reviews", args=[self.user.username]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        