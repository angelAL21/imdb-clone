from django.urls import path, include
from rest_framework.routers import DefaultRouter
#from watchlist_app.api.views import movie_list, movie_details used in api crud @app_view
from watchlist_app.api.views import WatchlistListAPIVIEW, WatchlistDetailAPIVIEW, ReviewList, ReviewDetail, ReviewCreate, StreamPlatformVS, UserReview, WatchListGV


router = DefaultRouter()
router.register('stream', StreamPlatformVS, basename='streamplatform')

urlpatterns = [
    
    path('list/', WatchlistListAPIVIEW.as_view(), name='movie-list' ),
    path('<int:pk>/', WatchlistDetailAPIVIEW.as_view(), name='movie-detail'),
    
    path('', include(router.urls)),
    
    #path('stream/', StreamPlatformAPIVIEW.as_view(), name='stream'),
    #path('stream/<int:pk>', StreamPlatformDetailAPIVIEW.as_view(), name='stream-detail'),
    
    path('<int:pk>/reviews/', ReviewList.as_view(), name= 'review-list'), #particular movie all reviews
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'), #individual review
    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'), #creating a review for x movie.
    
    # path('review/',ReviewList.as_view(), name='review-list'), #with mixins. get all reviews
    # path('review/<int:pk>',ReviewDetail.as_view(), name='review-list'), #with mixins. get single review
    
    #path('reviews/<str:username>/', UserReview.as_view(), name='user-review-detail') #used for userreview view #1
    path('reviews/', UserReview.as_view(), name='user-review-detail'), #used for UserReview #2. we dont pass the username, its auto-generated.
    #http://127.0.0.1:8000/watch/reviews/=username=USERNAME
    
    path('list2/', WatchListGV.as_view(), name = 'watch-list'),

]
