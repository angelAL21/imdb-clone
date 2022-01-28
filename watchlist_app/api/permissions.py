from rest_framework import permissions

class IsAdminOrReadOnly(permissions.IsAdminUser): #cant modify review is not admin, can see if user or not.
    def has_permission(self, request,view):
        if request.method in permissions.SAFE_METHODS:
            #permissions for read only
            return True
        else:
            return bool(request.user and request.user.is_staff)
    
class IsReviewUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request,view, obj): 
        if request.method in permissions.SAFE_METHODS:
            #permissions for read only
            return True
        else:
            return obj.review_user == request.user
            
        