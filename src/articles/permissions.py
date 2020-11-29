from django.conf import settings

from rest_framework.permissions import BasePermission


class AllowEditors(BasePermission):
    """
    Allow only requests with valid 'Authorization: Token XXXX' header and token
    value in EDITOR_TOKENS setting
    """

    def has_permission(self, request, view):
        # get token from 'Authorization: Token XXXXX' header
        token_header = request.META.get("HTTP_AUTHORIZATION", "")

        try:
            _, token_value = token_header.split(" ")
        except ValueError:
            return False

        return token_value in settings.EDITOR_TOKENS
