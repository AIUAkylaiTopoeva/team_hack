from rest_framework.permissions import BasePermission
#permission - разрешение на что-либо
class IsActivePermission(BasePermission):     #проверяет активен аккаунт или нет
    def has_permission(self, request, view):      
        return bool(request.user and request.user.is_active)