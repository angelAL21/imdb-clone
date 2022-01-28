from rest_framework.test import APITestCase 
from rest_framework import status 
from django.urls import reverse 
from django.contrib.auth.models import User 
from rest_framework.authtoken.models import Token

#test for our register function
class RegisterTestCase(APITestCase):
    def test_register(self):
        #passing fake data but not into db. just dummy data.
        data={
            "username": "testcase",
            "email": "testcase@example.com",
            "password": "testcase",
            "password2": "testcase"
        }
        response =self.client.post(reverse('register'),data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        

#test for our login function 
class LoginLogOutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="example",
                                             password="password")
        
    def test_login(self):
        data={
            "username": "example",
            "password": "password"
        }
        response = self.client.post(reverse('login'),data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_logout(self):
        self.token = Token.objects.get(user__username="example")
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.token.key)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)