
from typing import Iterable
from rest_framework.permissions import BasePermission

class CustomPermissionFilter(BasePermission):
    
    
    def __init__(self, allowedMethods : Iterable = None,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.allowedMethod = allowedMethods
    
    
    
    def has_permission(self, request, view):
        return bool(request.method in self.allowedMethod or (request.user and request.user.is_authenticated))
    
    
    def __call__(self, *args, **kwds):
        return self