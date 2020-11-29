from django.db.models import F

from rest_framework import mixins, viewsets, permissions
from rest_framework.response import Response

from .models import Article
from .serializers import ArticleSerializer
from .permissions import AllowEditors


class ArticleViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    View set for creating, retrieving, updating and deleting Articles.
    Listing all Articles is disabled on purpose. Any request can retrieve
    Article but only those with valid tokens can edit/create/delete them.
    """

    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    def get_permissions(self):
        if self.action == "retrieve":
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [AllowEditors]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, *args, **kwargs):
        """
        Generic retrieve updated with incrementing views counter
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        instance_queryset = self.get_queryset().filter(uuid=instance.uuid)
        instance_queryset.update(views_count=F("views_count") + 1)

        return Response(serializer.data)
