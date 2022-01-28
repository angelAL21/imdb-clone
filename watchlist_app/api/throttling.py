from rest_framework.throttling import UserRateThrottle

class ReviewCreateThrottle(UserRateThrottle):
    scope = 'review-create'
    
class ReviewListCreateThrottle(UserRateThrottle):
    scope ='review-list'
    