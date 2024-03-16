from rest_framework.permissions import BasePermission

class IsGymOwner(BasePermission):
    def has_permission(self, request, view):
        # Comprueba si el usuario tiene el rol de dueño
        return request.user and request.user.is_authenticated and request.user.rol == 'owner'
