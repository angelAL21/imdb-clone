from ast import arg
from rest_framework.test import APITestCase 
from rest_framework import status 
from django.urls import reverse 
from django.contrib.auth.models import User 
from rest_framework.authtoken.models import Token

from watchlist_app.api import serializers
from watchlist_app import models 


class StreamPlatformCase(APITestCase):
    #we logged as a user and for access other test cases.
    def setUp(self):
        self.user= User.objects.create_user(username="example", password="123")
        self.token = Token.objects.get(user__username= self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token'+ self.token.key)
        
        #creating a dummy stream.
        self.stream = models.StreamPlatform.objects.create(name="netflix", about="platform", website="https://www.netflix.com")
    
    #As a normal user i try to create a stream platform. but only admin can.
    def test_streamplatform_create(self):
        data= {
            "name": "netflix",
            "about": "stream platform",
            "website": "https://netflix.com"
        }
        response = self.client.post(reverse('streamplatform-list'), data)  
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
     
     
     #as a normal user i try to get the request of all movies.   
    def test_streamplatform_get(self):
        response=self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    #trying to access individual platform
    def test_streamplatform_individual(self):
        response=self.client.get(reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    #watchlist testcase.
class WatchListTestCase(APITestCase):
    
    def setUp(self):
        #creating dummy platform.
        self.user= User.objects.create_user(username="example", password="123")
        self.token = Token.objects.get(user__username= self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token'+ self.token.key)
        
        #creating a dummy stream.
        self.stream = models.StreamPlatform.objects.create(name="netflix", about="platform", website="https://www.netflix.com")
        
        #creating a dummy movie. 
        self.watchlist = models.WatchList.objects.create(platform=self.stream, title="example movie1", storyline="good", active=True)
        
        
    #creating movie.
    def test_watchlist_create(self):
        data = {
            "platform": self.stream,
            "title": "example movie 1",
            "storyline": "good",
            "active": True,
        }
        response = self.client.post(reverse('movie-list'), data)  
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
    #gettig list of all movies.
    def test_watchlist(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

      
    #getting one movie.
    def test_watchlist_individual(self):
        response = self.client.get(reverse('movie-detail', args=(self.watchlist.id,)))  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.get().title, "example movie1") #checking if movie name is ok.
        
        
#review test case
class ReviewTestCase(APITestCase):
    def setUp(self):
        
        #creating dummy user.
        self.user= User.objects.create_user(username="example", password="123")
        self.token = Token.objects.get(user__username= self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.token.key)
        
         #creating a dummy stream.
        self.stream = models.StreamPlatform.objects.create(name="netflix", about="platform", website="https://www.netflix.com")
        
        #creating a dummy movie. 
        self.watchlist = models.WatchList.objects.create(platform=self.stream, title="example movie1", storyline="good", active=True)
        self.watchlist2 = models.WatchList.objects.create(platform=self.stream, title="example movie1", storyline="good", active=True)
        
        self.review = models.Review.objects.create(review_user=self.user, rating=5, description="great movie", watchlist=self.watchlist2, active=True)
    
    #testing creating of review.
    def test_review_create(self):
        data={
            "review_user": self.user,
            "rating": 5,
            "description": "greatttt",
            "watchlist": self.watchlist,
            "active": True
        }
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #if trying to review same movie again.
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)  
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    #review as an unauthenticated user.
    def test_review_create_unauth(self):
        data={
            "review_user": self.user,
            "rating": 5,
            "description": "greatttt",
            "watchlist": self.watchlist,
            "active": True
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    #update review.
    def test_review_update(self):
        data={
            "review_user": self.user,
            "rating": 4,
            "description": "greatttt- updated",
            "watchlist": self.watchlist,
            "active": True
        }
        response = self.client.put(reverse('review-detail', args=(self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
     
    #get all reviews.   
    def test_review_lsit(self):
        respose = self.client.get(reverse('review-list', args=(self.watchlist.id,)))  
        self.assertEqual(respose.status_code, status.HTTP_200_OK)
        
    #get one review.
    def test_review_ind(self):
        response = self.client.get(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_user(self):
        response= self.client.get('/watch/review/?username' + 'self.user.username')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        