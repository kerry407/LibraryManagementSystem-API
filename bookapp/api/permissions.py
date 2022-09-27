from rest_framework import permissions 

class AdminOrAuthenticatedUser(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True 
        else:
            return request.user and request.user.is_staff 
        
class ReviewUserOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True 
        else:
            return obj.review_user == request.user 
        
class AdminOrReadOnly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user.is_staff