from rest_framework.response import Response #response
from django.shortcuts import get_object_or_404
#from rest_framework.decorators import api_view #decorator for crud and api_view regular View Class.
from watchlist_app.models import Review, WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from rest_framework import status #for status codes.
from rest_framework.views import APIView #used for crud APIView 
# from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from watchlist_app.api.permissions import IsReviewUserOrReadOnly, IsAdminOrReadOnly

from rest_framework.throttling import AnonRateThrottle, ScopedRateThrottle #,UserRateThrottle

from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListCreateThrottle

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters

from watchlist_app.api.pagination import WatchCPagination #WatchListOffsetPag #WatchListPagination 

class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer
    
    # def get_queryset(self): for parameters with the username #1
    #     pk = self.kwargs['username']
    #     return Review.objects.filter(review_user__username=pk) #we get the review for x movie.
    
    def get_queryset(self): #2
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(review_user__username=username)

#generic class-based views
class ReviewList(generics.ListAPIView):
    #queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    #permission_classes = [IsAuthenticated] #cant access if not logged to the list, only by one.
    throttle_classes = [ReviewListCreateThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk) #we get the review for x movie.
        
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly] #read only even if or logged
    #throttle_classes = [UserRateThrottle, AnonRateThrottle] #instead of creating a file throttle, we can do it directly with throttle_classes
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'
    
    
    
#for creating a review.
class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)
        
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user = review_user)
        
        if review_queryset.exists():
            raise ValidationError("you have already reviewed this movie")
        
        #calification of movie.
        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2
        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()
        
        serializer.save(watchlist=watchlist, review_user=review_user)
        

# #with mixins.
# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

# #with mixins
# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

#API CRUD WITH APIView Class-based, and subclasses.
class WatchlistListAPIVIEW(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request):
        movies = WatchList.objects.all() #get all movies.
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)
    
    def post(self, request): #post a new movie.
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid(): #if data is valid...
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
#RECOMENDED
class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    #pagination_class = WatchListPagination
    #pagination_class = WatchListOffsetPag
    pagination_class = WatchCPagination
    
    
    #filter_backends = [DjangoFilterBackend]
    #filter_backends = [filters.SearchFilter] #for breaking a word and not exact match.
    # filter_backends = [filters.OrderingFilter] #for ordering our filter
    # ordering_fields =['avg_rating']
    #filterset_fields = ['title', 'platform__name']
    #search_fields = ['title', 'platform__name']

        
class WatchlistDetailAPIVIEW(APIView): #for put, delete, get.
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error': ' not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)
    
    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        #sending information to json after deleting
        return Response(status=status.HTTP_204_NO_CONTENT)


#crud apiview for streamplatform

class StreamPlatformAPIVIEW(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request):
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform, many=True, context={'request': request}) #context for hyperlink in serializer
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

#with viewclass.      
class StreamPlatformVS(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer

#routing, api with viewsets.s
# class StreamPlatformVS(viewsets.ViewSet):
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)
    
#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        
class StreamPlatformDetailAPIVIEW(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'Error': ' not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StreamPlatformSerializer(platform, context={'request': request}) #context for hyperlink in serializer
        return Response(serializer.data)
    
    def put(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        



##CRUD WITH methods and api_view regular View classes
#FUNCTION BASED VIEWS 


# #get all movies
# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
    
#     #creating a new movie instance and validating data.
#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# #GET
# # get one movie with its id
# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, pk):
#     if request.method == 'GET':
#         #if movie does not exist.
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({'Error': 'movie not found'}, status=status.HTTP_404_NOT_FOUND)
        
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
    
#     #receiving data from client and checking if it is valid or not.
#     #PUT
#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk=pk) #check if its same object and not creating new one
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     #delete movie with id
#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         #sending information to json after deleting
#         return Response(status=status.HTTP_204_NO_CONTENT)