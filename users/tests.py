from rest_framework.test import APITestCase
from django.urls import reverse 
from django.contrib.auth.models import User 
from rest_framework import status 


class AccountCreationTest(APITestCase):
    
    def test_create_account(self):
        data = {
            "username": "testusername",
            "email": "testemail@gmail.com",
            "password": "Akpororo1",
            "password2": "Akpororo1"
        }         
        response = self.client.post(reverse("create_account"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
class LoginAndLogoutTest(APITestCase):
    
    def setUp(self):
        user = User.objects.create_user(
                                        username="testusername", 
                                        email="testemail@gmail.com", 
                                        password="Akpororo1"
                                        )
        
    def test_login(self):
        data = {
            "username": "testusername",
            "password": "Akpororo1"
        }
        response = self.client.post(reverse("token_obtain_pair"), data)
        data_access = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        return data_access["refresh"]
    
    def test_refresh_token(self):
        token = self.test_login()
        credential = {
            "refresh": token
        }
        response = self.client.post(reverse("token_refresh"), credential)
        access = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
