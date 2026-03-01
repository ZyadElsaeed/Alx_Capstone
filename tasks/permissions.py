from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Custom permission that only allows the owner of an object to access it.

    Expects the model instance to have a `user` attribute referencing the owner.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
