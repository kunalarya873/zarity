from rest_framework.permissions import BasePermission

class IsDoctor(BasePermission):
    """
    Permission for Doctor users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'doctor'

class IsPatient(BasePermission):
    """
    Permission for Patient users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'patient'
