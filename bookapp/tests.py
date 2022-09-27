from django.forms import SlugField
from rest_framework.test import APITestCase 
from rest_framework import status
from .models import Book, Author, Category, Country
from django.urls import reverse 
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
# Create your tests here.

class AuthorTestCase(APITestCase):
    
    def setUp(self):
        self.author = Author.objects.create(first_name="Kerry", last_name="Onyeogo", middle_name="Nwaka")
        self.user = User.objects.create_user(username="exampleuser", email="example@gmail.com", password="Akpororo1")
        refresh = RefreshToken.for_user(self.user)
        access_token = refresh.access_token
        self.client.credentials(HTTP_AUTHORIZATION= f"Bearer {access_token}")
        
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
        

class CategoryTestCase(APITestCase):
    
    def setUp(self):
        self.category = Category.objects.create(name="Folklore")
        self.user = User.objects.create_user(username="exampleuser", email="example@gmail.com", password="Akpororo1")
        refresh = RefreshToken.for_user(self.user)
        access_token = refresh.access_token
        self.client.credentials(HTTP_AUTHORIZATION= f"Bearer {access_token}")
        
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
        response = self.client.get(reverse("category-detail", args=[self.category.name]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)  
        
    def test_update_individual_category(self):
        data = {
            "name": "History"
        }
        response = self.client.put(reverse("category-detail", args=[self.category.name]), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_delete_individual_category(self):
        response = self.client.delete(reverse("category-detail", args=[self.category.name]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        
class BookTestCase(APITestCase):

    def setUp(self):
        self.category1 = Category.objects.create(name="Folklore")
        self.category2 = Category.objects.create(name="History")
        self.author = Author.objects.create(first_name="Kerry", last_name="Onyeogo", middle_name="Nwaka")
        self.country1 = Country.objects.create(name="Germany", code="DE")
        self.country2 = Country.objects.create(name="United Kingdom", code="UK")
        self.user = User.objects.create_user(username="exampleuser", email="example@gmail.com", password="Akpororo1")
        refresh = RefreshToken.for_user(self.user)
        access_token = refresh.access_token
        self.client.credentials(HTTP_AUTHORIZATION= f"Bearer {access_token}")
        
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