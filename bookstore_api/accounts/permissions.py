from rest_framework import permissions

class AdminPermission(permissions.BasePermission):
    edit_methods = ("PUT", "PATCH", "GET", "LIST")

    def has_permission(self, request, view):
        if request.user.groups.filter(name="ADMIN").exists():
            return True
        return False


class StockManagerPermission(permissions.BasePermission):
    edit_methods = ("PUT", "PATCH", "GET", "LIST")

    def has_permission(self, request, view):
        if request.user.groups.filter(name="STOCK_MANAGER").exists():
            return True
        return False